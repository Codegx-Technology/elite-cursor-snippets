# backend/mock_db.py

from datetime import datetime, timedelta
from typing import List, Dict, Any

# Conceptual in-memory storage for mock data
mock_sla_records = {
    "tenant_1": {
        "2025-07": {
            "uptime_percentage": 99.9,
            "avg_response_time_ms": 150,
            "error_rate": 0.01,
            "incidents": 2
        },
        "2025-08": {
            "uptime_percentage": 99.95,
            "avg_response_time_ms": 120,
            "error_rate": 0.005,
            "incidents": 1
        }
    }
}

mock_billing_transactions = {
    "user_1": [
        {"transaction_id": "txn_001", "amount": 25.0, "currency": "KES", "timestamp": (datetime.utcnow() - timedelta(days=30)).isoformat(), "provider": "Mpesa"},
        {"transaction_id": "txn_002", "amount": 19.99, "currency": "USD", "timestamp": (datetime.utcnow() - timedelta(days=15)).isoformat(), "provider": "Stripe"}
    ],
    "user_2": [
        {"transaction_id": "txn_003", "amount": 50.0, "currency": "KES", "timestamp": (datetime.utcnow() - timedelta(days=45)).isoformat(), "provider": "Mpesa"}
    ]
}

mock_usage_records = {
    "user_1": [
        {"feature": "video_generation", "count": 5, "timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat()},
        {"feature": "image_generation", "count": 150, "timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat()}
    ],
    "user_2": [
        {"feature": "video_generation", "count": 10, "timestamp": (datetime.utcnow() - timedelta(days=10)).isoformat()},
        {"feature": "audio_generation", "count": 20, "timestamp": (datetime.utcnow() - timedelta(days=8)).isoformat()}
    ]
}

mock_reconciliation_reports = {
    "2025-07": {
        "total_revenue": 10000.0,
        "total_expenses": 2000.0,
        "net_profit": 8000.0,
        "transactions_count": 150,
        "discrepancies": [
            {"type": "payment_mismatch", "details": "Transaction ID 12345 amount mismatch"}
        ]
    },
    "2025-08": {
        "total_revenue": 12000.0,
        "total_expenses": 2500.0,
        "net_profit": 9500.0,
        "transactions_count": 180,
        "discrepancies": []
    }
}

class MockDB:
    def get_sla_record(self, tenant_id: str, month: str) -> Optional[Dict[str, Any]]:
        return mock_sla_records.get(tenant_id, {}).get(month)

    def get_billing_transactions(self, user_id: str) -> List[Dict[str, Any]]:
        return mock_billing_transactions.get(user_id, [])

    def get_usage_records(self, user_id: str) -> List[Dict[str, Any]]:
        return mock_usage_records.get(user_id, [])

    def get_reconciliation_report(self, month: str) -> Optional[Dict[str, Any]]:
        return mock_reconciliation_reports.get(month)

mock_db = MockDB()
