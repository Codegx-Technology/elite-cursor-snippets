#!/usr/bin/env python3
"""
payment_integration.py
Payment integration for Shujaa Studio API
Following elite-cursor-snippets patterns for Kenya-specific requirements
"""

import os
import requests
import json
import hashlib
import time
from typing import Dict, Any, Optional
from datetime import datetime
import base64

class PaymentIntegration:
    def __init__(self):
        """Initialize payment integration"""
        self.mpesa_consumer_key = os.getenv("MPESA_CONSUMER_KEY", "")
        self.mpesa_consumer_secret = os.getenv("MPESA_CONSUMER_SECRET", "")
        self.mpesa_passkey = os.getenv("MPESA_PASSKEY", "")
        self.mpesa_business_shortcode = os.getenv("MPESA_BUSINESS_SHORTCODE", "")
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", "")
        
        # M-Pesa API endpoints
        self.mpesa_base_url = "https://sandbox.safaricom.co.ke"  # Change to production URL
        self.stripe_base_url = "https://api.stripe.com/v1"
    
    def _get_mpesa_access_token(self) -> Optional[str]:
        """Get M-Pesa access token"""
        try:
            # Create auth string
            auth_string = f"{self.mpesa_consumer_key}:{self.mpesa_consumer_secret}"
            auth_bytes = auth_string.encode('ascii')
            base64_auth = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Basic {base64_auth}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.mpesa_base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json().get('access_token')
            return None
            
        except Exception as e:
            print(f"Error getting M-Pesa access token: {e}")
            return None
    
    def _generate_mpesa_password(self, timestamp: str) -> str:
        """Generate M-Pesa password"""
        password_string = f"{self.mpesa_business_shortcode}{self.mpesa_passkey}{timestamp}"
        password_bytes = password_string.encode('ascii')
        return base64.b64encode(password_bytes).decode('ascii')
    
    def initiate_mpesa_payment(self, phone_number: str, amount: int, 
                              reference: str, description: str = "Shujaa Studio Credits") -> Dict[str, Any]:
        """Initiate M-Pesa STK Push payment"""
        try:
            # Get access token
            access_token = self._get_mpesa_access_token()
            if not access_token:
                return {
                    "success": False,
                    "message": "Failed to get M-Pesa access token"
                }
            
            # Generate timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = self._generate_mpesa_password(timestamp)
            
            # Prepare request payload
            payload = {
                "BusinessShortCode": self.mpesa_business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": self.mpesa_business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://your-domain.com/mpesa/callback",
                "AccountReference": reference,
                "TransactionDesc": description
            }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.mpesa_base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "checkout_request_id": result.get("CheckoutRequestID"),
                    "merchant_request_id": result.get("MerchantRequestID"),
                    "response_code": result.get("ResponseCode"),
                    "response_description": result.get("ResponseDescription"),
                    "customer_message": result.get("CustomerMessage")
                }
            else:
                return {
                    "success": False,
                    "message": f"M-Pesa API error: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"M-Pesa payment failed: {str(e)}"
            }
    
    def check_mpesa_payment_status(self, checkout_request_id: str) -> Dict[str, Any]:
        """Check M-Pesa payment status"""
        try:
            access_token = self._get_mpesa_access_token()
            if not access_token:
                return {
                    "success": False,
                    "message": "Failed to get M-Pesa access token"
                }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.mpesa_base_url}/mpesa/stkpushquery/v1/query",
                json={
                    "BusinessShortCode": self.mpesa_business_shortcode,
                    "CheckoutRequestID": checkout_request_id,
                    "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
                    "Password": self._generate_mpesa_password(datetime.now().strftime('%Y%m%d%H%M%S'))
                },
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "result_code": result.get("ResultCode"),
                    "result_desc": result.get("ResultDesc"),
                    "amount": result.get("Amount"),
                    "mpesa_receipt_number": result.get("MpesaReceiptNumber"),
                    "transaction_date": result.get("TransactionDate")
                }
            else:
                return {
                    "success": False,
                    "message": f"Status check failed: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Status check failed: {str(e)}"
            }
    
    def create_stripe_payment_intent(self, amount: int, currency: str = "usd", 
                                   description: str = "Shujaa Studio Credits") -> Dict[str, Any]:
        """Create Stripe payment intent"""
        try:
            headers = {
                'Authorization': f'Bearer {self.stripe_secret_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'amount': amount * 100,  # Convert to cents
                'currency': currency,
                'description': description,
                'automatic_payment_methods[enabled]': 'true'
            }
            
            response = requests.post(
                f"{self.stripe_base_url}/payment_intents",
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "client_secret": result.get("client_secret"),
                    "payment_intent_id": result.get("id"),
                    "amount": result.get("amount"),
                    "currency": result.get("currency")
                }
            else:
                return {
                    "success": False,
                    "message": f"Stripe API error: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Stripe payment failed: {str(e)}"
            }
    
    def confirm_stripe_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Confirm Stripe payment"""
        try:
            headers = {
                'Authorization': f'Bearer {self.stripe_secret_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.get(
                f"{self.stripe_base_url}/payment_intents/{payment_intent_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "status": result.get("status"),
                    "amount": result.get("amount"),
                    "currency": result.get("currency"),
                    "payment_method": result.get("payment_method")
                }
            else:
                return {
                    "success": False,
                    "message": f"Payment confirmation failed: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Payment confirmation failed: {str(e)}"
            }
    
    def process_credit_purchase(self, user_id: str, amount: int, 
                              payment_method: str, phone_number: str = None) -> Dict[str, Any]:
        """Process credit purchase with M-Pesa or Stripe"""
        try:
            if payment_method.lower() == "mpesa":
                if not phone_number:
                    return {
                        "success": False,
                        "message": "Phone number required for M-Pesa payment"
                    }
                
                # Format phone number for M-Pesa (254XXXXXXXXX)
                if phone_number.startswith("0"):
                    phone_number = "254" + phone_number[1:]
                elif phone_number.startswith("+254"):
                    phone_number = phone_number[1:]
                
                reference = f"SHUJAA_{user_id}_{int(time.time())}"
                
                result = self.initiate_mpesa_payment(
                    phone_number=phone_number,
                    amount=amount,
                    reference=reference,
                    description=f"Shujaa Studio {amount} Credits"
                )
                
                if result["success"]:
                    return {
                        "success": True,
                        "payment_method": "mpesa",
                        "checkout_request_id": result["checkout_request_id"],
                        "reference": reference,
                        "message": "M-Pesa payment initiated. Check your phone for STK Push."
                    }
                else:
                    return result
                    
            elif payment_method.lower() == "stripe":
                result = self.create_stripe_payment_intent(
                    amount=amount,
                    description=f"Shujaa Studio {amount} Credits"
                )
                
                if result["success"]:
                    return {
                        "success": True,
                        "payment_method": "stripe",
                        "client_secret": result["client_secret"],
                        "payment_intent_id": result["payment_intent_id"],
                        "message": "Stripe payment intent created."
                    }
                else:
                    return result
                    
            else:
                return {
                    "success": False,
                    "message": "Unsupported payment method"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Payment processing failed: {str(e)}"
            }

# Global instance
payment_integration = PaymentIntegration()
