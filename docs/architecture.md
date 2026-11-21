# Architecture

The project separates deterministic processing from optional AI orchestration.

- `lead_pipeline.py`: repeatable rule-based lead scoring.
- `agents.py`: CrewAI agent definitions using Gemini.
- `tasks.py`: sequential research, validation and scoring tasks.
- `crew.py`: executes the multi-agent workflow.
- `invoice_audit.py`: Pydantic validation and duplicate detection.
- `api.py`: FastAPI endpoints.
- `main.py`: runs deterministic demo pipelines.

The CrewAI workflow is optional and requires a Gemini API key.
The deterministic workflow is the default reproducible demo.
