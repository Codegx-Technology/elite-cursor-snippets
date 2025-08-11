import asyncio
import json
import requests
import hmac
import hashlib
import time
from datetime import datetime
from typing import Dict, Any

from logging_setup import get_logger

logger = get_logger(__name__)

class WebhookSimulator:
    """
    // [TASK]: Implement a conceptual webhook simulator
    // [GOAL]: Facilitate testing of webhook receiving endpoints
    // [ELITE_CURSOR_SNIPPET]: aihandle
    """
    def __init__(self, target_url: str, secret: str = "your_webhook_secret_key"):
        self.target_url = target_url
        self.secret = secret
        logger.info(f"WebhookSimulator initialized. Target URL: {self.target_url}")

    def _generate_signature(self, payload_body: bytes) -> str:
        """
        Generates an HMAC-SHA256 signature for the webhook payload.
        """
        return hmac.new(self.secret.encode('utf-8'), payload_body, hashlib.sha256).hexdigest()

    async def send_webhook(self, event_type: str, data: Dict[str, Any], simulate_failure: bool = False):
        """
        Sends a simulated webhook to the target URL.
        """
        payload = {
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "simulate_failure": simulate_failure # For testing retry logic
        }
        payload_json = json.dumps(payload)
        payload_bytes = payload_json.encode('utf-8')

        signature = self._generate_signature(payload_bytes)

        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature # Custom header for signature
        }

        logger.info(f"Simulating sending webhook for event '{event_type}' to {self.target_url}")
        try:
            # In a real scenario, use aiohttp for async requests
            response = requests.post(self.target_url, data=payload_bytes, headers=headers)
            response.raise_for_status()
            logger.info(f"✅ Webhook sent successfully. Status: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send webhook: {e}")
            raise

# Example Usage (conceptual)
async def main():
    # Replace with your actual webhook receiving endpoint
    simulator = WebhookSimulator(target_url="http://localhost:8000/webhook/payment_status")

    # Simulate a payment completed event
    await simulator.send_webhook(
        event_type="payment_completed",
        data={
            "user_id": "user_123",
            "transaction_id": "txn_abc",
            "status": "completed",
            "amount": 99.99,
            "currency": "USD",
            "plan_name": "premium"
        }
    )

    # Simulate a payment failed event with simulated failure for retry testing
    await simulator.send_webhook(
        event_type="payment_failed",
        data={
            "user_id": "user_456",
            "transaction_id": "txn_def",
            "status": "failed",
            "amount": 19.99,
            "currency": "KES",
            "plan_name": "basic"
        },
        simulate_failure=True
    )

if __name__ == "__main__":
    asyncio.run(main())
