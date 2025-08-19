# Monetization Tiers → Routing & Pinning

This document outlines the monetization tiers implemented in the Shujaa Studio platform, detailing how they influence model routing, version pinning, and overall service behavior.

## Tier Definitions

Each tier is defined in `billing_models.py` and configured in `billing_models.py` (via `get_default_plans()`). Key attributes for each tier include:

*   **`tier_code`**: Unique identifier for the tier (`FREE`, `PRO`, `BUSINESS`, `ENTERPRISE`).
*   **`model_policy`**: Dictates how models are selected and routed for users in this tier.
    *   `defaultRouting`: (`latest` | `pinned` | `allow_minor`) - Strategy for model version selection.
    *   `pinned`: Specific model versions forced for certain task types (e.g., `"tts": {model:"xtts-v2","version":"a1b2c3d4"}`).
    *   `providers`: Ordered list of preferred providers for each task type (e.g., `"tts": ["elevenlabs","xtts","local"]`).
*   **`quotas`**: Defines usage limits.
    *   `monthly`: Monthly limits for tokens, audio seconds, video minutes, and jobs.
    *   `concurrency`: Maximum concurrent jobs allowed.
    *   `rateLimit`: Request per minute (RPM), requests per second (RPS), and burst limits.
*   **`priority`**: Maps to job queue priority (`low` | `standard` | `high` | `critical`).
*   **`cost_caps`**: Controls spending limits.
    *   `monthlyUsd`: Monthly cost cap in USD.
    *   `hardStop`: (`true` | `false`) - Whether to block tasks once the cost cap is reached.
*   **`visibility`**: Controls access to certain model types.
    *   `showBetaModels`: (`true` | `false`) - Access to beta models.
    *   `allowUnverified`: (`true` | `false`) - Access to unverified models.

### Default Tier Mappings:

*   **FREE**: `latest`, `low` priority, modest quotas.
*   **PRO**: `allow_minor`, `standard` priority, higher quotas.
*   **BUSINESS**: `allow_minor` + canary, `high` priority, even higher caps.
*   **ENTERPRISE**: `pinned` only, `critical` priority, negotiated caps.

## Admin Playbook

Administrators can manage tier policies and monitor usage through the system. Key actions include:

1.  **Pin models per tier**: Ensure specific model versions are used for critical tasks for certain tiers (e.g., Enterprise).
2.  **Order providers**: Define the fallback order of AI providers for each task type to ensure resilience and cost-efficiency.
3.  **Set quotas / rate limits / cost caps**: Configure usage and spending limits for each tier.
4.  **Watch alerts, approve canaries, rollback if needed**: Monitor system notifications for threshold breaches, new model versions, and performance issues, taking action as necessary.

## Core Benefits

This monetization tier system provides:

*   **Predictable Costs**: Through cost caps and alerts, preventing unexpected overages.
*   **Predictable Quality**: Via pinned models, ensuring consistent performance for high-tier users.
*   **SLA by Tier**: Achieved through priority queues, guaranteeing better service for higher tiers.
*   **Provider Resilience**: Ordered fallback mechanisms ensure continuous service even if a primary provider fails.
*   **Frictionless Growth**: Allows putting FREE users on “latest” models for rapid iteration while ENTERPRISE users remain on stable, blessed versions.

## Technical Implementation Details

*   **Tier Schema Upgrade**: Implemented in `billing_models.py` using Python dataclasses.
*   **Policy Resolver Middleware**: `backend/middleware/policy_resolver.py` intercepts requests, determines the user's effective policy, and attaches it to the request context. This middleware also enforces rate limits and initial quotas.
*   **Job Priority Queues**: Celery is used to route jobs to different queues (`critical`, `high`, `standard`, `low`) based on the user's tier priority. Configured in `celery_app.py` and integrated in `backend/core/jobs.py`.
*   **Quotas & Rate Limits**: Managed via Redis in `backend/services/quota_service.py`, enforcing monthly quotas and sliding window rate limits.
*   **Cost Meter**: `backend/costs/provider_costs.py` loads cost tables from `provider_costs.yml`. `backend/core/jobs_hooks.py` records `UsageCost` entries in the database post-job execution.
*   **Version Pinning + Emergency Freeze**: Logic in `backend/ai_routing/router.py` (`execute_with_fallback`) forces pinned model versions based on tier policy. `backend/ai_models/model_store.py` includes a global emergency freeze flag.
*   **Notifications & Thresholds**: `backend/watchers/billing_watcher.py` checks for quota and cost cap thresholds, sending notifications via `notify_admin()`.
*   **Model Watcher**: `watchers/model_watcher.py` continuously monitors for new LLM model and TTS voice versions from external providers (e.g., Hugging Face). It records new versions in the database (`ModelVersion`, `VoiceVersion`) and notifies administrators, enabling informed decisions on model updates without automatic upgrades for pinned tiers.
*   **Client Isolation & Shared Models**: Conceptual design involves dedicated model serving processes (e.g., via `backend/ai_routing/providers/local_provider.py`) and IPC.
*   **E2E Tests**: Located in `tests/backend/tiers/test_monetization.py` covering various scenarios.

