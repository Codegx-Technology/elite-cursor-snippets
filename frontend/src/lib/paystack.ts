// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: Paystack payment integration for Kenya-first payment processing
// [GOAL]: Implement comprehensive Paystack integration with proper error handling
// [TASK]: Create payment flows, subscription management, and transaction handling

import { useState } from 'react';

export interface PaystackConfig {
  publicKey: string;
  currency: 'KES' | 'USD' | 'GHS' | 'ZAR';
  channels: ('card' | 'bank' | 'ussd' | 'qr' | 'mobile_money' | 'bank_transfer')[];
}

export interface PaystackCustomer {
  email: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

export interface PaystackTransaction {
  amount: number; // Amount in kobo (for KES, multiply by 100)
  email: string;
  currency?: string;
  reference?: string;
  callback_url?: string;
  plan?: string;
  invoice_limit?: number;
  metadata?: Record<string, any>;
  channels?: string[];
  split_code?: string;
  subaccount?: string;
  transaction_charge?: number;
  bearer?: 'account' | 'subaccount';
}

export interface PaystackResponse {
  status: boolean;
  message: string;
  data?: any;
}

export interface PaystackVerificationResponse {
  status: boolean;
  message: string;
  data: {
    id: number;
    domain: string;
    status: 'success' | 'failed' | 'abandoned';
    reference: string;
    amount: number;
    message: string;
    gateway_response: string;
    paid_at: string;
    created_at: string;
    channel: string;
    currency: string;
    ip_address: string;
    metadata: Record<string, any>;
    fees: number;
    customer: {
      id: number;
      first_name: string;
      last_name: string;
      email: string;
      phone: string;
    };
    authorization: {
      authorization_code: string;
      bin: string;
      last4: string;
      exp_month: string;
      exp_year: string;
      channel: string;
      card_type: string;
      bank: string;
      country_code: string;
      brand: string;
      reusable: boolean;
      signature: string;
    };
  };
}

class PaystackService {
  private config: PaystackConfig;
  private baseUrl = 'https://api.paystack.co';

  constructor(config: PaystackConfig) {
    this.config = config;
  }

  // Generate unique transaction reference
  generateReference(): string {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 15);
    return `shujaa_${timestamp}_${random}`;
  }

  // Convert amount to kobo (Paystack's smallest currency unit)
  toKobo(amount: number): number {
    return Math.round(amount * 100);
  }

  // Convert from kobo to main currency
  fromKobo(amount: number): number {
    return amount / 100;
  }

  // Initialize transaction
  async initializeTransaction(transaction: PaystackTransaction): Promise<PaystackResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/transaction/initialize`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...transaction,
          amount: this.toKobo(transaction.amount),
          currency: transaction.currency || this.config.currency,
          channels: transaction.channels || this.config.channels,
        }),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack initialization error:', error);
      return {
        status: false,
        message: 'Failed to initialize payment',
      };
    }
  }

  // Verify transaction
  async verifyTransaction(reference: string): Promise<PaystackVerificationResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/transaction/verify/${reference}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack verification error:', error);
      return {
        status: false,
        message: 'Failed to verify payment',
        data: {} as any,
      };
    }
  }

  // Create customer
  async createCustomer(customer: PaystackCustomer): Promise<PaystackResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/customer`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(customer),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack customer creation error:', error);
      return {
        status: false,
        message: 'Failed to create customer',
      };
    }
  }

  // Create subscription plan
  async createPlan(plan: {
    name: string;
    interval: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'biannually' | 'annually';
    amount: number;
    currency?: string;
    description?: string;
    send_invoices?: boolean;
    send_sms?: boolean;
    invoice_limit?: number;
  }): Promise<PaystackResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/plan`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...plan,
          amount: this.toKobo(plan.amount),
          currency: plan.currency || this.config.currency,
        }),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack plan creation error:', error);
      return {
        status: false,
        message: 'Failed to create plan',
      };
    }
  }

  // Create subscription
  async createSubscription(subscription: {
    customer: string;
    plan: string;
    authorization?: string;
    start_date?: string;
  }): Promise<PaystackResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/subscription`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscription),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack subscription creation error:', error);
      return {
        status: false,
        message: 'Failed to create subscription',
      };
    }
  }

  // Cancel subscription
  async cancelSubscription(code: string, token: string): Promise<PaystackResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/subscription/disable`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          token,
        }),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack subscription cancellation error:', error);
      return {
        status: false,
        message: 'Failed to cancel subscription',
      };
    }
  }

  // Get transaction history
  async getTransactions(customer?: string, status?: string, from?: string, to?: string): Promise<PaystackResponse> {
    try {
      const params = new URLSearchParams();
      if (customer) params.append('customer', customer);
      if (status) params.append('status', status);
      if (from) params.append('from', from);
      if (to) params.append('to', to);

      const response = await fetch(`${this.baseUrl}/transaction?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${process.env.PAYSTACK_SECRET_KEY}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Paystack transaction history error:', error);
      return {
        status: false,
        message: 'Failed to get transaction history',
      };
    }
  }
}

// Default Paystack configuration for Kenya
export const defaultPaystackConfig: PaystackConfig = {
  publicKey: process.env.NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY || '',
  currency: 'KES',
  channels: ['card', 'bank', 'ussd', 'mobile_money'],
};

// Create Paystack service instance
export const paystackService = new PaystackService(defaultPaystackConfig);

// Utility functions for frontend
export const paymentUtils = {
  formatAmount: (amount: number, currency: string = 'KES'): string => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency,
    }).format(amount);
  },

  validateEmail: (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  validatePhone: (phone: string): boolean => {
    // Kenya phone number validation
    const phoneRegex = /^(\+254|0)[17]\d{8}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
  },

  formatPhone: (phone: string): string => {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.startsWith('254')) {
      return `+${cleaned}`;
    }
    if (cleaned.startsWith('0')) {
      return `+254${cleaned.slice(1)}`;
    }
    return phone;
  },
};

// React hook for Paystack integration
export function usePaystack() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const initializePayment = async (transaction: PaystackTransaction) => {
    setIsLoading(true);
    setError(null);

    try {
      // Load Paystack script if not already loaded
      await PaystackService.loadScript();

      // Initialize payment
      const result = await paystackService.initializePayment(transaction);

      setIsLoading(false);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Payment failed';
      setError(errorMessage);
      setIsLoading(false);
      throw err;
    }
  };

  const verifyPayment = async (reference: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await paystackService.verifyTransaction(reference);
      setIsLoading(false);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Verification failed';
      setError(errorMessage);
      setIsLoading(false);
      throw err;
    }
  };

  return {
    initializePayment,
    verifyPayment,
    isLoading,
    error,
  };
}

// TypeScript declarations for Paystack
declare global {
  interface Window {
    PaystackPop: {
      setup: (config: any) => {
        openIframe: () => void;
      };
    };
  }
}

export default PaystackService;
