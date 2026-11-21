from fastapi import FastAPI, HTTPException
from src.lead_pipeline import process_leads
from src.invoice_audit import audit_invoices

app = FastAPI(
    title="CrewAI Enterprise Automation API",
    description="Demo API for lead processing and invoice auditing.",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/leads/process")
def leads_process():
    try:
        return process_leads()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/invoices/audit")
def invoices_audit():
    try:
        return audit_invoices()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
