from celery import Celery
from kombu import Queue
from config_loader import get_config

config = get_config()

# Celery App Instance
app = Celery(
    'shujaa_studio',
    broker=config.redis.url, # Assuming Redis is configured in config.yaml
    backend=config.redis.url # Using Redis as backend for result storage
)

# Define Priority Queues
app.conf.task_queues = (
    Queue('critical', routing_key='critical'),
    Queue('high', routing_key='high'),
    Queue('standard', routing_key='standard'),
    Queue('low', routing_key='low'),
)

# Map tiers to queues and set retry limits
# This mapping will be used by the task dispatching logic
PRIORITY_QUEUE_MAP = {
    "ENTERPRISE": {"queue": "critical", "retries": 5},
    "BUSINESS": {"queue": "high", "retries": 3},
    "PRO": {"queue": "standard", "retries": 2},
    "FREE": {"queue": "low", "retries": 1},
}

# Configure Dead-Letter Queues (DLQs) for each priority queue
# This is a simplified example. In a real setup, you might use separate DLQ names
# and more sophisticated routing for dead letters.
app.conf.task_routes = {
    '*': {'queue': 'standard'}, # Default queue
    'critical': {'queue': 'critical'},
    'high': {'queue': 'high'},
    'standard': {'queue': 'standard'},
    'low': {'queue': 'low'},
}

# Task retry policy (default for all tasks, can be overridden per task)
app.conf.task_acks_late = True # Acknowledge task after it's done
app.conf.task_reject_on_worker_lost = True # Requeue task if worker dies

# Auto-discover tasks in specified modules (e.g., 'backend.core.jobs')
app.autodiscover_tasks(['backend.core'])

# Example of a simple task (for testing purposes)
@app.task(bind=True)
def debug_task(self, message):
    print(f"Executing debug task: {message}")
    return f"Task {self.request.id} executed: {message}"
