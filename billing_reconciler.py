import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid
import random

from logging_setup import get_logger
from billing_models import BillingTransaction, UsageRecord, ReconciliationReport, SLARecord, get_user_subscription, get_default_plans
from enhanced_model_router import EnhancedModelRouter # To access historical performance

logger = get_logger(__name__)

class BillingReconciler:
    """
    // [TASK]: Implement conceptual billing reconciliation and reporting
    // [GOAL]: Reconcile usage data with billing transactions and generate reports
    // [ELITE_CURSOR_SNIPPET]: aihandle
    """
    def __init__(self, router: EnhancedModelRouter):
        self.router = router
        self.transactions: List[BillingTransaction] = []
        self.usage_records: List[UsageRecord] = []
        self.reconciliation_reports: Dict[str, ReconciliationReport] = {}
        self.plans = get_default_plans()
        self.cost_per_feature = {
            "text_gen": 0.001, # Cost per unit (e.g., per 1000 tokens)
            "image_gen": 0.01, # Cost per image
            "tts": 0.002, # Cost per unit (e.g., per 1000 characters)
            "stt": 0.003, # Cost per unit (e.g., per minute of audio)
            "youtube_upload": 0.05, # Flat fee per upload
            "analytics": 0.0, # Included in plan
            "crm_integration": 0.0 # Included in plan
        }

    def _get_feature_cost(self, feature: str, count: int) -> float:
        """Calculates the cost for a given feature usage."""
        return self.cost_per_feature.get(feature, 0.0) * count

    def record_usage(self, user_id: str, feature: str, count: int = 1):
        """Records a usage event."""
        record = UsageRecord(
            user_id=user_id,
            feature=feature,
            count=count,
            timestamp=datetime.now()
        )
        self.usage_records.append(record)
        logger.info(f"Recorded usage: User {user_id}, Feature {feature}, Count {count}")

    def record_transaction(self, user_id: str, amount: float, currency: str = "USD", provider: str = "Mpesa"):
        """Records a billing transaction."""
        transaction = BillingTransaction(
            transaction_id=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            currency=currency,
            timestamp=datetime.now(),
            provider=provider
        )
        self.transactions.append(transaction)
        logger.info(f"Recorded transaction: User {user_id}, Amount {amount} {currency} via {provider}")

    async def reconcile_month(self, month: str) -> ReconciliationReport:
        """
        Performs billing reconciliation for a given month.
        This is a conceptual implementation.
        """
        logger.info(f"Performing billing reconciliation for month: {month}")
        
        # Filter usage records and transactions for the given month
        start_date = datetime.strptime(month, "%Y-%m")
        end_date = start_date + timedelta(days=30) # Approximate month end

        monthly_usage = [
            rec for rec in self.usage_records 
            if start_date <= rec.timestamp < end_date
        ]
        monthly_transactions = [
            tx for tx in self.transactions 
            if start_date <= tx.timestamp < end_date
        ]

        # Calculate total expected usage cost
        total_usage_cost = 0.0
        user_usage_summary: Dict[str, Dict[str, int]] = {} # user_id -> feature -> count

        for usage_rec in monthly_usage:
            user_usage_summary.setdefault(usage_rec.user_id, {}).setdefault(usage_rec.feature, 0)
            user_usage_summary[usage_rec.user_id][usage_rec.feature] += usage_rec.count
        
        for user_id, features_usage in user_usage_summary.items():
            user_subscription = get_user_subscription(user_id) # Get user's plan
            plan = next((p for p in self.plans if p.name == user_subscription.plan_name), None)
            
            if plan:
                # For simplicity, assume all usage beyond free tier is billed
                # In a real system, this would be more complex (e.g., tiered pricing, overages)
                for feature, count in features_usage.items():
                    if feature in plan.features_enabled: # Assume features enabled by plan are covered by monthly cost
                        # For now, we'll just sum up all usage costs for simplicity
                        total_usage_cost += self._get_feature_cost(feature, count)
            else:
                # If no plan, bill all usage
                for feature, count in features_usage.items():
                    total_usage_cost += self._get_feature_cost(feature, count)

        # Calculate total billed amount
        total_billed = sum(tx.amount for tx in monthly_transactions)

        mismatches: List[str] = []
        tickets_created: List[str] = []

        # Simple mismatch detection
        if abs(total_billed - total_usage_cost) > 0.01: # Allow for small floating point differences
            mismatches.append(f"Total billed ({total_billed:.2f}) does not match total usage cost ({total_usage_cost:.2f}).")
            ticket_id = f"TICKET-{str(uuid.uuid4())[:8]}"
            tickets_created.append(ticket_id)
            logger.warning(f"Mismatch detected. Created ticket: {ticket_id}")

        report = ReconciliationReport(
            month=month,
            total_billed=total_billed,
            total_usage_cost=total_usage_cost,
            mismatches=mismatches,
            tickets_created=tickets_created
        )
        self.reconciliation_reports[month] = report
        logger.info(f"Reconciliation Report for {month}: Billed={total_billed:.2f}, Usage Cost={total_usage_cost:.2f}, Mismatches={len(mismatches)}")
        return report

    def get_reconciliation_report(self, month: str) -> Optional[ReconciliationReport]:
        """Retrieves a specific reconciliation report."""
        return self.reconciliation_reports.get(month)

    def get_all_reconciliation_reports(self) -> Dict[str, ReconciliationReport]:
        """Retrieves all generated reconciliation reports."""
        return self.reconciliation_reports

    async def generate_billing_report(self, month: str) -> Dict[str, Any]:
        """
        Generates a comprehensive billing report for a given month.
        This will combine SLA, usage, and reconciliation data.
        """
        logger.info(f"Generating comprehensive billing report for month: {month}")
        
        reconciliation_report = await self.reconcile_month(month)
        
        # Get SLA records for the month (assuming SLATracker is accessible or its data is passed)
        # For simplicity, we'll assume SLATracker is managed separately or its data is aggregated here.
        # In a real system, SLATracker would persist its data and this report would query it.
        
        # For now, let's just include the reconciliation report and a summary of usage
        report_summary = {
            "month": month,
            "reconciliation": {
                "total_billed": reconciliation_report.total_billed,
                "total_usage_cost": reconciliation_report.total_usage_cost,
                "mismatches_found": len(reconciliation_report.mismatches),
                "tickets_created": reconciliation_report.tickets_created
            },
            "usage_summary": {}, # user_id -> feature -> count
            "sla_summary": {} # tenant_id -> SLARecord summary
        }

        # Populate usage summary from self.usage_records for the month
        start_date = datetime.strptime(month, "%Y-%m")
        end_date = start_date + timedelta(days=30)
        for usage_rec in self.usage_records:
            if start_date <= usage_rec.timestamp < end_date:
                report_summary["usage_summary"].setdefault(usage_rec.user_id, {}).setdefault(usage_rec.feature, 0)
                report_summary["usage_summary"][usage_rec.user_id][usage_rec.feature] += usage_rec.count
        
        # To include SLA, we'd need access to SLATracker's records.
        # For now, this is a placeholder.
        # if self.router and hasattr(self.router, 'sla_tracker'):
        #     sla_record = self.router.sla_tracker.get_sla_record("some_tenant_id", month)
        #     if sla_record:
        #         report_summary["sla_summary"]["some_tenant_id"] = {
        #             "uptime_percentage": sla_record.uptime_percentage,
        #             "response_time_slo_met": sla_record.response_time_slo_met,
        #             "credits_due": sla_record.credits_due
        #         }

        logger.info(f"Comprehensive billing report generated for {month}.")
        return report_summary

# Example Usage (conceptual)
async def main():
    from enhanced_model_router import enhanced_router # Assuming enhanced_router is globally available
    reconciler = BillingReconciler(router=enhanced_router)

    # Simulate some usage
    reconciler.record_usage("user1", "text_gen", 10000)
    reconciler.record_usage("user1", "image_gen", 5)
    reconciler.record_usage("user2", "text_gen", 5000)
    reconciler.record_usage("user1", "youtube_upload", 1)

    # Simulate some transactions
    reconciler.record_transaction("user1", 15.00)
    reconciler.record_transaction("user2", 5.00)

    # Generate report for current month
    current_month = datetime.now().strftime("%Y-%m")
    report = await reconciler.generate_billing_report(current_month)
    logger.info(f"Generated Billing Report: {json.dumps(report, indent=2)}")

if __name__ == "__main__":
    import asyncio
    import json
    asyncio.run(main())