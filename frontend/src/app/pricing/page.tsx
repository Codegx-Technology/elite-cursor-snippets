'use client';

import { useEffect, useState } from 'react';
import Card from '@/components/Card';
import { FaCheck, FaCrown, FaFlag, FaMountain, FaRocket } from 'react-icons/fa6';
import GraceCountdownOverlay from '@/components/GraceCountdownOverlay';
import { useWidgetLoader } from '@/utils/widgetLoader';
import { usePlanGuard } from '@/context/PlanGuardContext'; // New import

// Import with error handling
let paymentUtils: any;
let usePaystack: any;

// Local types for plan and payment method to satisfy TS when using require()
type Plan = {
  id: string;
  name: string;
  price: number;
  currency: string;
  features: string[];
  video_credits?: number;
  image_credits?: number;
  audio_credits?: number;
  popular?: boolean;
  allowedModels?: string[];
  defaultPinnedModel?: string;
  maxRequestsPerMonth?: number;
  priorityLevel?: number;
  ttsVoices?: string[];
  rollbackWindowDays?: number;
  grace_period_hours?: number; // New field
};
type PaymentMethod = { id: string; name: string; description: string; icon: any };

// [SNIPPET]: thinkwithai + kenyafirst + surgicalfix + refactorintent + augmentsearch
// [CONTEXT]: Pricing page with Paystack integration and Kenya-first design
// [GOAL]: Create comprehensive pricing interface with real payment processing
// [TASK]: Implement subscription plans with Paystack payment flow and cultural authenticity

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [plans, setPlans] = useState<Plan[]>([]);
  const { initializePayment, isLoading, error } = usePaystack();

  const { planStatus, loading: planStatusLoading, error: planStatusError } = usePlanGuard(); // Use usePlanGuard hook

  // Load PlanGuardWidget using the loader
  const { component: PlanGuardWidgetComponent, allowed: planGuardWidgetAllowed, message: planGuardWidgetMessage } = useWidgetLoader("PlanGuardWidget", "test_user_id");
  const { component: PlanGuardDashboardWidgetComponent, allowed: planGuardDashboardWidgetAllowed, message: planGuardDashboardWidgetMessage } = useWidgetLoader("PlanGuardDashboardWidget", "test_user_id");

  // Load plans from API with graceful fallback to static tiers
  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const res = await fetch('/api/tiers', { cache: 'no-store' });
        if (!res.ok) throw new Error(`status ${res.status}`);
        const data = await res.json();
        // Expecting API shape: [{ id, name, priceKesMonthly, perks:[], quotas:{ videos, images, audio } }]
        const mapped: Plan[] = (data?.tiers || data || []).map((t: any) => ({
          id: t.id,
          name: t.name,
          price: Number(t.priceKesMonthly ?? t.price ?? 0),
          currency: 'KES',
          features: Array.isArray(t.perks) ? t.perks : [],
          video_credits: t?.quotas?.videos ?? undefined,
          image_credits: t?.quotas?.images ?? undefined,
          audio_credits: t?.quotas?.audio ?? undefined,
          popular: t?.popular ?? false,
          grace_period_hours: t?.grace_period_hours ?? undefined, // New field
        }));

        if (!cancelled && mapped.length) {
          setPlans(mapped);
          return;
        }
      } catch (e) {
        console.warn('Failed to load /api/tiers, falling back to static tiers', e);
      }

      // Fallback to backend-aligned static tiers
      const fallback: Plan[] = [
        {
          id: 'starter',
          name: 'Starter',
          price: 500,
          currency: 'KES',
          features: [
            '5k requests / month',
            'Pinned: gpt-4o-mini',
            'Voice: XTTS v2',
            'Email support',
            '3-day rollback window',
          ],
          video_credits: 10,
          image_credits: 100,
          audio_credits: 60,
          popular: false,
          allowedModels: ['gpt-4o-mini'],
          defaultPinnedModel: 'gpt-4o-mini',
          maxRequestsPerMonth: 5000,
          priorityLevel: 1,
          ttsVoices: ['xtts-v2'],
          rollbackWindowDays: 3,
        },
        {
          id: 'pro',
          name: 'Pro',
          price: 2500,
          currency: 'KES',
          features: [
            '50k requests / month',
            'Pinned: gpt-4o, gpt-5',
            'Voice: XTTS v2, Elevenlabs Pro',
            'Priority support',
            '7-day rollback window',
          ],
          video_credits: 40,
          image_credits: 500,
          audio_credits: 360,
          popular: true,
          allowedModels: ['gpt-4o', 'gpt-5'],
          defaultPinnedModel: 'gpt-5',
          maxRequestsPerMonth: 50000,
          priorityLevel: 2,
          ttsVoices: ['xtts-v2', 'elevenlabs-pro'],
          rollbackWindowDays: 7,
        },
        {
          id: 'enterprise',
          name: 'Enterprise',
          price: 15000,
          currency: 'KES',
          features: [
            '500k requests / month',
            'Custom models',
            'Voice: All premium voices',
            'Dedicated support',
            '30-day rollback window',
          ],
          video_credits: -1,
          image_credits: -1,
          audio_credits: -1,
          popular: false,
          allowedModels: ['gpt-5', 'gpt-5.5', 'custom-finetunes'],
          defaultPinnedModel: 'gpt-5.5',
          maxRequestsPerMonth: 500000,
          priorityLevel: 5,
          ttsVoices: ['xtts-v2', 'elevenlabs-pro', 'elevenlabs-multi'],
          rollbackWindowDays: 30,
        },
      ];
      if (!cancelled) setPlans(fallback);
    };
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSubscribe = async (planId: string) => {
    setSelectedPlan(planId);
    
    const plan = plans.find((p: any) => p.id === planId);
    if (!plan) return;

    try {
      // Notify backend billing with selected tier before payment
      try {
        await fetch('/api/tiers/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tierId: planId, billing_cycle: billingCycle }),
        });
      } catch (e) {
        console.warn('Backend subscribe call failed, continuing with payment', e);
      }

      await initializePayment({
        amount: billingCycle === 'yearly' ? plan.price * 10 : plan.price, // 2 months free on yearly
        email: 'user@example.com', // This should come from user context
        currency: plan.currency,
        metadata: {
          plan_id: planId,
          billing_cycle: billingCycle,
          user_id: 'user_123' // This should come from user context
        }
      });
      
      // Payment successful - handle subscription activation
      console.log('Payment successful for plan:', planId);
    } catch (err) {
      console.error('Payment failed:', err);
    } finally {
      setSelectedPlan(null);
    }
  };

  const getDiscountedPrice = (price: number) => {
    return billingCycle === 'yearly' ? price * 10 : price; // 2 months free on yearly
  };

  return (
    <div className="space-y-8">
      {/* Kenya-First Header */}
      <div className="bg-gradient-to-r from-green-600 via-red-600 to-black p-8 rounded-xl text-white shadow-lg text-center">
        <div className="flex items-center justify-center space-x-4 mb-4">
          <FaFlag className="text-3xl" />
          <FaMountain className="text-3xl text-yellow-300" />
        </div>
        <h1 className="text-3xl font-bold mb-2">Choose Your Kenya-First Plan 🇰🇪</h1>
        <p className="text-green-100 text-lg">
          Empower your storytelling with authentic African AI technology
        </p>
      </div>

      {/* Billing Toggle */}
      <Card className="p-6">
        <div className="flex items-center justify-center">
          <div className="bg-gray-100 p-1 rounded-lg flex">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-2 rounded-md transition-all duration-200 ${
                billingCycle === 'monthly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-6 py-2 rounded-md transition-all duration-200 relative ${
                billingCycle === 'yearly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Yearly
              <span className="absolute -top-2 -right-2 bg-green-600 text-white text-xs px-2 py-1 rounded-full">
                Save 17%
              </span>
            </button>
          </div>
        </div>
      </Card>

      {/* Pricing Plans */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {plans.map((plan: Plan) => (
          <Card
            key={plan.id}
            className={`relative overflow-hidden transition-all duration-300 hover:shadow-xl ${
              plan.popular ? 'ring-2 ring-green-600 scale-105' : ''
            }`}
          >
            {plan.popular && (
              <div className="absolute top-0 left-0 right-0 bg-green-600 text-white text-center py-2 text-sm font-medium">
                <FaCrown className="inline mr-2" />
                Most Popular
              </div>
            )}

            <div className={`p-6 ${plan.popular ? 'pt-12' : ''}`}>
              {/* Plan Header */}
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <div className="mb-4">
                  <span className="text-3xl font-bold text-gray-900">
                    {paymentUtils.formatAmount(getDiscountedPrice(plan.price), plan.currency)}
                  </span>
                  <span className="text-gray-600">
                    /{billingCycle === 'yearly' ? 'year' : 'month'}
                  </span>
                </div>
                {billingCycle === 'yearly' && (
                  <p className="text-sm text-green-600 font-medium">
                    Save {paymentUtils.formatAmount(plan.price * 2, plan.currency)} per year!
                  </p>
                )}
              </div>

              {/* Features */}
              <div className="space-y-3 mb-8">
                {plan.features.map((feature: string, index: number) => (
                  <div key={index} className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">{feature}</span>
                  </div>
                ))}
                {plan.allowedModels && plan.allowedModels.length > 0 && (
                  <div className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">
                      Allowed Models: {plan.allowedModels.join(', ')}
                    </span>
                  </div>
                )}
                {plan.defaultPinnedModel && (
                  <div className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">
                      Default Pinned Model: {plan.defaultPinnedModel}
                    </span>
                  </div>
                )}
                {plan.maxRequestsPerMonth && (
                  <div className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">
                      Max Requests/Month: {plan.maxRequestsPerMonth.toLocaleString()}
                    </span>
                  </div>
                )}
                {plan.priorityLevel && (
                  <div className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">
                      Priority Level: {plan.priorityLevel}
                    </span>
                  </div>
                )}
                {plan.ttsVoices && plan.ttsVoices.length > 0 && (
                  <div className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">
                      TTS Voices: {plan.ttsVoices.join(', ')}
                    </span>
                  </div>
                )}
                {plan.rollbackWindowDays && (
                  <div className="flex items-start space-x-3">
                    <FaCheck className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-700 text-sm">
                      Rollback Window: {plan.rollbackWindowDays} days
                    </span>
                  </div>
                )}
              </div>

              {/* Credits Info */}
              <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <h4 className="font-medium text-gray-900 mb-2">Monthly Credits</h4>
                <div className="grid grid-cols-3 gap-2 text-sm">
                  <div className="text-center">
                    <div className="font-bold text-blue-600">
                      {plan.video_credits === -1 ? '∞' : plan.video_credits}
                    </div>
                    <div className="text-gray-600">Videos</div>
                  </div>
                  <div className="text-center">
                    <div className="font-bold text-green-600">
                      {plan.image_credits === -1 ? '∞' : plan.image_credits}
                    </div>
                    <div className="text-gray-600">Images</div>
                  </div>
                  <div className="text-center">
                    <div className="font-bold text-purple-600">
                      {plan.audio_credits === -1 ? '∞' : plan.audio_credits}
                    </div>
                    <div className="text-gray-600">Audio</div>
                  </div>
                </div>
              </div>

              {/* Subscribe Button */}
              <button
                onClick={() => handleSubscribe(plan.id)}
                disabled={isLoading && selectedPlan === plan.id}
                className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
                  plan.popular
                    ? 'bg-green-600 hover:bg-green-700 text-white'
                    : 'bg-gray-900 hover:bg-gray-800 text-white'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {isLoading && selectedPlan === plan.id ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Processing...</span>
                  </div>
                ) : (
                  `Subscribe to ${plan.name}`
                )}
              </button>
            </div>
          </Card>
        ))}
      </div>

      {/* Payment Methods */}
      <Card className="p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4 text-center">
          Secure Payment Methods 🔒
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {(paymentUtils.getKenyaPaymentMethods() as PaymentMethod[]).map((method: PaymentMethod) => (
            <div key={method.id} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl mb-2">{method.icon}</div>
              <div className="font-medium text-gray-900 text-sm">{method.name}</div>
              <div className="text-xs text-gray-600">{method.description}</div>
            </div>
          ))}
        </div>
        <p className="text-center text-sm text-gray-600 mt-4">
          Powered by Paystack • Secure & trusted by millions across Africa
        </p>
      </Card>

      {/* FAQ Section */}
      <Card className="p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4 text-center">
          Frequently Asked Questions
        </h3>
        <div className="space-y-4">
          <div>
            <h4 className="font-medium text-gray-900 mb-1">Can I change my plan anytime?</h4>
            <p className="text-sm text-gray-600">
              Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-1">What happens to unused credits?</h4>
            <p className="text-sm text-gray-600">
              Unused credits roll over to the next month for up to 3 months, ensuring you never lose value.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-1">Is there a free trial?</h4>
            <p className="text-sm text-gray-600">
              Yes! All new users get 3 free video generations to experience our Kenya-first AI technology.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-1">Do you offer refunds?</h4>
            <p className="text-sm text-gray-600">
              We offer a 30-day money-back guarantee if you're not satisfied with our service.
            </p>
          </div>
        </div>
      </Card>

      {/* Cultural Footer */}
      <div className="bg-gradient-to-r from-yellow-400 via-red-500 to-green-600 p-6 rounded-lg text-white text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <FaFlag className="text-xl" />
          <span className="font-bold">Proudly Kenyan</span>
          <FaRocket className="text-xl" />
        </div>
        <p className="text-sm">
          🌍 Supporting African creators • 🎬 Celebrating heritage • 🇰🇪 Harambee spirit
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <Card className="p-4 bg-red-50 border border-red-200">
          <p className="text-red-800 text-center">{error}</p>
        </Card>
      )}

      {planStatus?.state === 'grace' && planStatus?.graceExpiresAt && (
        <GraceCountdownOverlay
          graceExpiresAt={planStatus.graceExpiresAt}
          onUpgradeClick={() => {
            // Handle upgrade click, e.g., scroll to pricing plans or open a modal
            console.log("Upgrade button clicked from grace overlay");
          }}
        />
      )}
    </div>
  );
}
