from typing import Dict, List, Any

# Conceptual registry for backend core modules and their required plan features.
# In a real system, this might be loaded from a database or configuration file.

MODULE_DEPENDENCIES: Dict[str, List[str]] = {
    "core_ai_engine": ["premium_ai_access"], # Example: requires a premium AI feature
    "analytics_processor": ["analytics_plus"], # Example: requires advanced analytics
    "realtime_data_stream": ["enterprise_features"], # Example: requires enterprise plan
    "nlp_core": ["premium_nlp"], # Example: requires premium NLP
    "data_viz_pro": ["premium_data_viz"], # Example: requires premium data visualization
}

# Mapping of conceptual features to actual plan allowed_models/features
# This would typically be managed by the PlanGuard itself or a related service
# For this conceptual registry, we'll assume these map to allowed_models in PlanGuard
CONCEPTUAL_FEATURE_TO_PLAN_MAP: Dict[str, List[str]] = {
    "premium_ai_access": ["gpt-5", "gpt-5.5"], # Maps to allowed_models
    "analytics_plus": ["analytics"], # Maps to features_enabled
    "enterprise_features": ["dedicated_instance"], # Maps to features_enabled
    "premium_nlp": ["custom-finetunes"], # Maps to allowed_models
    "premium_data_viz": ["custom-finetunes"], # Maps to allowed_models
}

def get_module_dependencies(module_name: str) -> List[str]:
    return MODULE_DEPENDENCIES.get(module_name, [])
