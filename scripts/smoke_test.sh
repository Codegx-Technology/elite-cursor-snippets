#!/usr/bin/env bash
set -e
pytest -q
python - <<'PY'
from pipeline_orchestrator import PipelineOrchestrator
import asyncio

orchestrator = PipelineOrchestrator()
asyncio.run(orchestrator.run_pipeline('general_prompt', 'A simple test prompt'))
PY
echo "Smoke tests passed"
