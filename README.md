# CrewAI Enterprise Portfolio

A modular enterprise automation demonstration combining multi-agent B2B lead analysis, invoice auditing, Pydantic validation and FastAPI.

## Features
- CrewAI agents for lead research, validation and scoring.
- Deterministic lead processing when AI execution is not enabled.
- Pydantic invoice validation.
- Duplicate invoice detection and financial audit checks.
- Optional Gemini model integration through CrewAI.
- FastAPI endpoints for lead processing and invoice auditing.
- CSV and JSON reports.
- Automated unit tests.
- Fictional demonstration data.

## Architecture
1. Lead pipeline: loads fictional leads, validates fields and calculates scores.
2. CrewAI: coordinates research, validation and scoring tasks when enabled.
3. Invoice audit: validates invoice records and identifies duplicate IDs.
4. FastAPI: exposes processing functions as HTTP endpoints.
5. Outputs: stores generated CSV and JSON reports.

## Installation
```bash
pip install -r requirements.txt
```

## Run deterministic pipelines
```bash
python -m src.main
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Run API
```bash
uvicorn src.api:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

## Optional Gemini + CrewAI execution

Set your Gemini API key as an environment variable:
```bash
export GEMINI_API_KEY="your_key"
```

Then run:
```bash
python -m src.crew
```

The CrewAI workflow uses Gemini through CrewAI's LLM interface. AI execution requires a valid API key, network access and a model supported by the installed CrewAI/provider versions. The deterministic pipeline does not require an API key.

## API Endpoints
- `GET /health` - service status
- `POST /leads/process` - run lead processing
- `POST /invoices/audit` - run invoice auditing

## Data and limitations
All included names, companies, emails and invoice records are fictional. This project does not scrape real websites or verify real businesses. Lead scoring is rule-based and does not guarantee lead quality. Invoice checks demonstrate basic validation, not professional accounting advice.

## Technology
Python, CrewAI, Gemini API, Pydantic, FastAPI, CSV, JSON, unittest.

## Test coverage
The deterministic unit test suite covers lead validation and scoring, invoice validation, duplicate detection and output generation.

Previously recorded verification: 8 deterministic unit tests passed. Live Gemini/CrewAI execution and API endpoint integration are separate checks and should only be described as verified after a successful run in the current environment.

## Repository
https://github.com/razibleads10-design/crewai-enterprise-portfolio
