# backend/core_modules/module_registry.py

from typing import List

def get_module_dependencies(module_name: str) -> List[str]:
    """
    Placeholder function to return dependencies for a given module.
    In a real system, this would load from a configuration or a database.
    """
    # Example dependencies for demonstration
    if module_name == "some_module":
        return ["feature_a", "model_x"]
    elif module_name == "another_module":
        return ["feature_b"]
    return []
