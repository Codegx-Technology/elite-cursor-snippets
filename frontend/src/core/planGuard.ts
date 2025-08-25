import { PlanStatus } from "@/widgets/PlanGuardWidget/types"; // Assuming this type is still relevant
import { fetchPlanStatus } from "@/widgets/PlanGuardWidget/planService"; // Assuming this service is still relevant

// Define Entitlement type
export type Entitlement = {
  key: string;
  level: 'free' | 'pro' | 'enterprise';
  limits?: Record<string, number>;
};

// Cache for plan status to avoid excessive API calls
let cachedPlan: { tier: string; entitlements: Entitlement[] } | null = null;
let lastFetchTime: number = 0;
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes TTL

// SuperAdmin usernames for bypass
const SUPERADMIN_USERS = ['peter', 'apollo'];

/**
 * Fetches and returns the current plan and entitlements.
 * Implements caching and graceful fallback if API fails.
 * @param ctx Context object, e.g., { userId: string, userRole?: string }
 */
export async function getCurrentPlan(ctx: { userId: string; userRole?: string }): Promise<{ tier: string; entitlements: Entitlement[] }> {
  const now = Date.now();

  // Check cache first
  if (cachedPlan && (now - lastFetchTime < CACHE_TTL_MS)) {
    return cachedPlan;
  }

  try {
    // Fetch plan status from backend
    const planStatus: PlanStatus = await fetchPlanStatus(ctx.userId);

    // Map PlanStatus to our internal Entitlement structure
    const entitlements: Entitlement[] = [
      { key: 'core_features', level: 'free' }, // Example: basic features are always free
      { key: 'video_generation', level: 'free', limits: { minutes: planStatus.quota.videoMins } },
      { key: 'audio_generation', level: 'free', limits: { minutes: planStatus.quota.audioMins } },
      { key: 'api_calls', level: 'free', limits: { tokens: planStatus.quota.tokens } },
    ];

    // Add more entitlements based on planName or specific features
    if (planStatus.planName.toLowerCase().includes('pro') || planStatus.planName.toLowerCase().includes('enterprise')) {
      entitlements.push({ key: 'premium_models', level: 'pro' });
      entitlements.push({ key: 'advanced_analytics', level: 'pro' });
    }
    if (planStatus.planName.toLowerCase().includes('enterprise')) {
      entitlements.push({ key: 'enterprise_features', level: 'enterprise' });
      entitlements.push({ key: 'dedicated_support', level: 'enterprise' });
    }

    cachedPlan = { tier: planStatus.planName, entitlements };
    lastFetchTime = now;
    return cachedPlan;

  } catch (error) {
    console.error("PlanGuard: Failed to fetch plan from API. Falling back to defaults.", error);
    // Graceful fallback: provide default entitlements if API fails
    const defaultPlan: { tier: string; entitlements: Entitlement[] } = {
      tier: "Fallback (Free)",
      entitlements: [
        { key: 'core_features', level: 'free' },
        { key: 'video_generation', level: 'free', limits: { minutes: 5 } },
        { key: 'audio_generation', level: 'free', limits: { minutes: 10 } },
        { key: 'api_calls', level: 'free', limits: { tokens: 1000 } },
      ],
    };
    cachedPlan = defaultPlan; // Cache fallback plan for TTL
    lastFetchTime = now;
    return defaultPlan;
  }
}

/**
 * Checks if a user can use a specific feature.
 * @param featureKey The key of the feature (e.g., 'video_generation', 'premium_models', 'models:gpt-4o').
 * @param ctx Context object, e.g., { userId: string, userRole?: string }
 */
export function canUse(featureKey: string, ctx: { userId: string; userRole?: string }): { ok: boolean; reason?: string } {
  // SuperAdmin bypass
  if (ctx.userRole === 'admin' || SUPERADMIN_USERS.includes(ctx.userId)) { // Assuming userId is username for superadmins
    return { ok: true, reason: 'BYPASS_SUPERADMIN' };
  }

  if (!cachedPlan) {
    return { ok: false, reason: 'API_DOWN' }; // Or trigger a fetch if not already loading
  }

  const entitlement = cachedPlan.entitlements.find(e => e.key === featureKey);

  if (entitlement) {
    // Basic check: if entitlement exists, it's allowed. More complex logic can go here.
    return { ok: true };
  }

  // Handle specific feature keys like 'models:gpt-4o'
  if (featureKey.startsWith('models:')) {
    const modelName = featureKey.split(':')[1];
    const modelEntitlement = cachedPlan.entitlements.find(e => e.key === 'premium_models');
    if (modelEntitlement && modelEntitlement.level === 'pro') { // Example: all premium models are 'pro'
      return { ok: true };
    }
    return { ok: false, reason: 'NOT_ENTITLED' };
  }
  
  return { ok: false, reason: 'NOT_ENTITLED' };
}

/**
 * Checks if a user can download a specific resource.
 * @param resourceKey The key of the resource (e.g., 'model:gpt-4o', 'widget:premium_widget').
 * @param ctx Context object, e.g., { userId: string, userRole?: string }
 */
export function canDownload(resourceKey: string, ctx: { userId: string; userRole?: string }): { ok: boolean; reason?: string } {
  // SuperAdmin bypass
  if (ctx.userRole === 'admin' || SUPERADMIN_USERS.includes(ctx.userId)) {
    return { ok: true, reason: 'BYPASS_SUPERADMIN' };
  }

  if (!cachedPlan) {
    return { ok: false, reason: 'API_DOWN' };
  }

  // Example: All downloads require at least a 'pro' plan
  if (cachedPlan.tier.toLowerCase().includes('free')) {
    return { ok: false, reason: 'NOT_ENTITLED' };
  }

  // More granular checks based on resourceKey can be added here
  if (resourceKey.startsWith('model:')) {
    const modelName = resourceKey.split(':')[1];
    const modelEntitlement = cachedPlan.entitlements.find(e => e.key === 'premium_models');
    if (modelEntitlement && modelEntitlement.level === 'pro') {
      return { ok: true };
    }
    return { ok: false, reason: 'NOT_ENTITLED' };
  }

  return { ok: true }; // Default to allowed if no specific rule
}

/**
 * Requires a feature to be usable, throwing an error if not.
 * @param featureKey The key of the feature.
 * @param ctx Context object.
 */
export function requireOrThrow(featureKey: string, ctx: { userId: string; userRole?: string }): void {
  const check = canUse(featureKey, ctx);
  if (!check.ok) {
    throw new Error(`PLAN_GUARD_BLOCK: ${check.reason || 'Access denied'}`);
  }
}

// Function to invalidate cache (e.g., on login/logout or plan change)
export function invalidatePlanCache() {
  cachedPlan = null;
  lastFetchTime = 0;
}

// Example of how to use it in a component (conceptual)
/*
import { useAuth } from '@/context/AuthContext'; // Assuming you have an AuthContext
import { getCurrentPlan, canUse } from '@/core/planGuard';

function MyComponent() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const [planInfo, setPlanInfo] = useState(null);

  useEffect(() => {
    if (isAuthenticated && user) {
      getCurrentPlan({ userId: user.id, userRole: user.role }).then(setPlanInfo);
    }
  }, [isAuthenticated, user]);

  if (isLoading || !planInfo) return <p>Loading plan...</p>;

  const canGenerateVideo = canUse('video_generation', { userId: user.id, userRole: user.role }).ok;

  return (
    <div>
      <p>Current Plan: {planInfo.tier}</p>
      {canGenerateVideo ? (
        <button>Generate Video</button>
      ) : (
        <p>Upgrade to generate videos.</p>
      )}
    </div>
  );
}
*/
