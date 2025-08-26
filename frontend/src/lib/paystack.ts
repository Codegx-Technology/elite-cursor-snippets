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
  metadata?: Record<string, unknown>;
  channels?: string[];
  split_code?: string;
  subaccount?: string;
  transaction_charge?: number;
  bearer?: 'account' | 'subaccount';
}

export interface PaystackResponse {
  status: boolean;
  message: string;
  data?: unknown;
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

  // Load Paystack inline script in browser (no-op on server)
  static async loadScript(): Promise<void> {
    if (typeof window === 'undefined') return; // SSR guard
    if ((window as any).PaystackPop) return;
    await new Promise<void>((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://js.paystack.co/v1/inline.js';
      script.async = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Failed to load Paystack script'));
      document.body.appendChild(script);
    });
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

  // Backward-compatible alias used by usePaystack()
  async initializePayment(transaction: PaystackTransaction): Promise<PaystackResponse> {
    return this.initializeTransaction(transaction);
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
        data: {},
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
  /**
   * Return subscription plans shown on the Pricing page
   * Keeping data local/offline-friendly and Kenya-first by defaulting to KES
   */
  getSubscriptionPlans: () => [
    {
      id: 'starter',
      name: 'Starter',
      price: 2500,
      currency: 'KES',
      features: ['10 Videos', '50 Images', '20 Audio tracks', 'Basic Support'],
      video_credits: 10,
      image_credits: 50,
      audio_credits: 20,
      popular: false,
    },
    {
      id: 'pro',
      name: 'Pro',
      price: 6500,
      currency: 'KES',
      features: [
        '40 Videos',
        '200 Images',
        '120 Audio tracks',
        'Priority Support',
        'Kenya-first Templates',
      ],
      video_credits: 40,
      image_credits: 200,
      audio_credits: 120,
      popular: true,
    },
    {
      id: 'business',
      name: 'Business',
      price: 14500,
      currency: 'KES',
      features: [
        'Unlimited Videos',
        'Unlimited Images',
        'Unlimited Audio tracks',
        'Dedicated Support',
        'Team Collaboration',
      ],
      video_credits: -1,
      image_credits: -1,
      audio_credits: -1,
      popular: false,
    },
  ],

  /**
   * Kenya-first payment methods to display on Pricing page
   * Icons are simple emoji/text to avoid React dependency in this lib
   */
  getKenyaPaymentMethods: () => [
    {
      id: 'mpesa',
      name: 'M-Pesa',
      description: 'Pay via mobile money',
      icon: '📱',
    },
    {
      id: 'card',
      name: 'Debit/Credit Card',
      description: 'Visa, Mastercard supported',
      icon: '💳',
    },
    {
      id: 'bank_transfer',
      name: 'Bank Transfer',
      description: 'Secure bank transfers',
      icon: '🏦',
    },
    {
      id: 'ussd',
      name: 'USSD',
      description: 'Pay with short code',
      icon: '🔢',
    },
  ],

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
      setup: (config: {
        key: string;
        email: string;
        amount: number;
        ref?: string;
        callback?: (response: any) => void; // This callback response can be complex, keeping as any for now
        onClose?: () => void;
        channels?: string[];
        currency?: string;
        metadata?: Record<string, unknown>;
      }) => {
        openIframe: () => void;
      };
    };
  }
}

export default PaystackService;
