import json
from pathlib import Path
from src.lead_pipeline import process_leads
from src.invoice_audit import audit_invoices

ROOT = Path(__file__).resolve().parents[1]

def main():
    (ROOT / "outputs").mkdir(exist_ok=True)
    lead_result = process_leads()
    invoice_result = audit_invoices()

    report = {
        "project": "CrewAI Enterprise Portfolio",
        "execution_mode": "deterministic_demo",
        "lead_pipeline": lead_result,
        "invoice_audit": {
            "total_records": invoice_result["total_records"],
            "valid_invoices": invoice_result["valid_invoices"],
            "invalid_invoices": invoice_result["invalid_invoices"],
            "duplicate_invoice_ids": invoice_result["duplicate_invoice_ids"],
            "valid_amount_total": invoice_result["valid_amount_total"]
        }
    }

    path = ROOT / "outputs" / "execution_report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print("\nDeterministic demo completed.")

if __name__ == "__main__":
    main()
