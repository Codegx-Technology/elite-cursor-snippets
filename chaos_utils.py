import time
import random
import os
from logging_setup import get_logger
from typing import Literal, Optional

logger = get_logger(__name__)

class ChaosInjector:
    def __init__(self):
        logger.info("ChaosInjector initialized.")

    def inject_latency(self, duration_ms: int):
        """Simulates network latency by pausing execution."""
        # // [TASK]: Simulate network latency
        # // [GOAL]: Test system resilience to network delays
        # // [ELITE_CURSOR_SNIPPET]: perfcheck
        logger.warning(f"Injecting {duration_ms}ms latency...")
        time.sleep(duration_ms / 1000.0)
        logger.warning(f"Latency injection complete.")

    def inject_cpu_spike(self, duration_s: int, intensity: float = 0.5):
        """Simulates a CPU spike by performing a busy-wait."""
        # // [TASK]: Simulate CPU spike
        # // [GOAL]: Test system resilience to CPU contention
        # // [ELITE_CURSOR_SNIPPET]: perfcheck
        logger.warning(f"Injecting CPU spike for {duration_s}s with intensity {intensity}...")
        end_time = time.time() + duration_s
        while time.time() < end_time:
            if random.random() < intensity:
                _ = [i*i for i in range(10000)] # Busy-wait
        logger.warning(f"CPU spike injection complete.")

    def inject_memory_hog(self, size_mb: int, duration_s: int):
        """Simulates a memory hog by allocating a large block of memory."""
        # // [TASK]: Simulate memory hog
        # // [GOAL]: Test system resilience to OOM scenarios
        # // [ELITE_CURSOR_SNIPPET]: perfcheck
        logger.warning(f"Injecting memory hog of {size_mb}MB for {duration_s}s...")
        # Create a byte array to consume memory
        _ = bytearray(size_mb * 1024 * 1024)
        time.sleep(duration_s)
        logger.warning(f"Memory hog injection complete.")
        # The allocated memory will be garbage collected when the function exits

    def inject_error_rate(self, probability: float = 0.5):
        """Simulates an increased error rate by raising an exception randomly."""
        # // [TASK]: Simulate increased error rate
        # // [GOAL]: Test system resilience to transient errors
        # // [ELITE_CURSOR_SNIPPET]: errorcheck
        if random.random() < probability:
            logger.error(f"Injecting random error with probability {probability}...")
            raise RuntimeError("Injected chaos error!")
        logger.debug("No error injected.")

    def inject_scenario(self, scenario_type: Literal["latency", "cpu_spike", "memory_hog", "error_rate"], **kwargs):
        """Injects a specific chaos scenario."""
        logger.info(f"Injecting chaos scenario: {scenario_type} with args: {kwargs}")
        if scenario_type == "latency":
            self.inject_latency(kwargs.get("duration_ms", 100))
        elif scenario_type == "cpu_spike":
            self.inject_cpu_spike(kwargs.get("duration_s", 5), kwargs.get("intensity", 0.5))
        elif scenario_type == "memory_hog":
            self.inject_memory_hog(kwargs.get("size_mb", 100), kwargs.get("duration_s", 5))
        elif scenario_type == "error_rate":
            self.inject_error_rate(kwargs.get("probability", 0.5))
        else:
            logger.error(f"Unknown chaos scenario type: {scenario_type}")
            raise ValueError("Unknown chaos scenario type")

# Initialize the injector
chaos_injector = ChaosInjector()

# Example usage (for testing)
if __name__ == "__main__":
    # Mock config for testing (if needed by get_logger)
    class MockLoggingConfig:
        level = "INFO"
        log_file = "logs/test_chaos.log"
        max_bytes = 10485760
        backup_count = 5
        enable_audit_log = False
    class MockConfig:
        logging = MockLoggingConfig()
    
    # Temporarily override global config for testing
    from config_loader import config as original_config
    from logging_setup import config as logging_config_ref
    logging_config_ref = MockConfig() # Direct assignment to global config in logging_setup
    
    print("--- Testing Chaos Scenarios ---")
    
    try:
        chaos_injector.inject_scenario("latency", duration_ms=200)
    except Exception as e:
        print(f"Caught expected error: {e}")

    try:
        chaos_injector.inject_scenario("cpu_spike", duration_s=2, intensity=0.8)
    except Exception as e:
        print(f"Caught expected error: {e}")

    try:
        chaos_injector.inject_scenario("memory_hog", size_mb=50, duration_s=2)
    except Exception as e:
        print(f"Caught expected error: {e}")

    try:
        chaos_injector.inject_scenario("error_rate", probability=1.0)
    except Exception as e:
        print(f"Caught expected error: {e}")

    try:
        chaos_injector.inject_scenario("error_rate", probability=0.0)
    except Exception as e:
        print(f"Caught expected error: {e}")

    print("--- Chaos Scenarios Test Complete ---")
    
    # Restore original config
    logging_config_ref = original_config