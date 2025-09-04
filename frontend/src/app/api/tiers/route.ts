import { NextResponse } from 'next/server';

// Simple in-app definition mirroring the UI fallback tiers.
// Replace later by fetching from backend service if available.

export const dynamic = 'force-dynamic'; // no static caching

interface BackendPlan {
  name: string;
  price: number;
  currency: string;
  features_enabled: string[];
  quotas: {
    monthly: {
      videoMins: number;
      tokens: number;
      audioSecs: number;
    };
  };
  popular?: boolean;
  model_policy: {
    allowed_models: string[];
    default_pinned_model: string;
    tts_voices: string[];
  };
  max_requests_per_month: number;
  priority_level: number;
  rollback_window_days: number;
}

export async function GET() {
  try {
    const response = await fetch('http://localhost:8000/api/plans', { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`Failed to fetch plans from backend: ${response.statusText}`);
    }
    const backendPlans: BackendPlan[] = await response.json();

    const tiers = backendPlans.map((plan) => ({
      id: plan.name.toLowerCase().replace(/ /g, '_'), // Generate ID from name
      name: plan.name,
      priceKesMonthly: plan.price, // Use 'price' from backend
      currency: plan.currency, // Use 'currency' from backend
      perks: plan.features_enabled, // Map features_enabled to perks
      quotas: {
        videos: plan.quotas.monthly.videoMins, // Map videoMins to videos
        images: plan.quotas.monthly.tokens, // Map tokens to images (adjust as needed)
        audio: plan.quotas.monthly.audioSecs, // Map audioSecs to audio
      },
      popular: plan.popular ?? false, // Assuming 'popular' might be a field in Plan
      allowedModels: plan.model_policy.allowed_models, // New field
      defaultPinnedModel: plan.model_policy.default_pinned_model, // New field
      maxRequestsPerMonth: plan.max_requests_per_month, // New field
      priorityLevel: plan.priority_level, // New field
      ttsVoices: plan.model_policy.tts_voices, // New field
      rollbackWindowDays: plan.rollback_window_days, // New field
    }));

    return NextResponse.json({ tiers }, { status: 200 });
  } catch (error) {
    console.error('Error fetching plans from backend:', error);
    return NextResponse.json({ message: 'Internal Server Error' }, { status: 500 });
  }
}
