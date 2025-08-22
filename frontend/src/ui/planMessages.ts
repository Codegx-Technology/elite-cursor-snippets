// frontend/src/ui/planMessages.ts

// Centralized user-facing copy for PlanGuard enforcement messages

export const PlanMessages = {
  NOT_ENTITLED: "Your plan doesn’t include this feature. Upgrade to continue.",
  UPDATE_BLOCKED: "Update locked: your plan doesn’t allow premium widget updates.",
  SLOWDOWN_FALLBACK: "We’ve applied a slower fallback model due to your plan. Upgrade for full speed.",
  VIEW_ONLY_MODE: "View-only mode: this widget is interactive on Pro+ plans.",
  API_DOWN_LIMITED_MODE: "Limited mode due to billing API connectivity. Some premium features may be restricted.",
  GENERIC_DENY: "Access denied due to plan restrictions. Please check your subscription.",
  GRACE_PERIOD_ACTIVE: "Your grace period is active. Please upgrade your plan soon.",
  GRACE_PERIOD_WARNING: "Your plan has expired. Some features may be limited. Upgrade now to avoid interruptions.",
  UPSELL_NUDGE_FREE_TO_PRO: "Unlock advanced features and higher limits with our Pro plan!",
  UPSELL_NUDGE_PRO_TO_ENTERPRISE: "Take your creativity to the next level with our Enterprise solutions!",
};

/**
 * Returns a user-friendly message based on a reason code.
 * @param reason The reason code (e.g., 'NOT_ENTITLED', 'API_DOWN').
 * @returns A user-friendly message string.
 */
export function getDenyMessage(reason: string): string {
  switch (reason) {
    case 'NOT_ENTITLED':
      return PlanMessages.NOT_ENTITLED;
    case 'UPDATE_BLOCKED':
      return PlanMessages.UPDATE_BLOCKED;
    case 'API_DOWN':
      return PlanMessages.API_DOWN_LIMITED_MODE;
    case 'VIEW_ONLY_BLOCKED': // Used by backend PlanGuard
      return PlanMessages.VIEW_ONLY_MODE;
    default:
      return PlanMessages.GENERIC_DENY;
  }
}

/**
 * Returns a user-friendly message for fallback scenarios.
 * @param context Context for the fallback (e.g., 'slowdown', 'view_only').
 * @returns A user-friendly message string.
 */
export function getFallbackMessage(context: string): string {
  switch (context) {
    case 'slowdown':
      return PlanMessages.SLOWDOWN_FALLBACK;
    case 'view_only':
      return PlanMessages.VIEW_ONLY_MODE;
    case 'api_down':
      return PlanMessages.API_DOWN_LIMITED_MODE;
    default:
      return "Some features may be limited due to your current plan.";
  }
}
