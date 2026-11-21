import csv
import json
from pathlib import Path
from collections import Counter
from pydantic import BaseModel, Field, field_validator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"

class Invoice(BaseModel):
    invoice_id: str = Field(min_length=1)
    vendor: str = Field(min_length=1)
    amount: float = Field(gt=0)
    currency: str = "USD"
    invoice_date: str

    @field_validator("invoice_date")
    @classmethod
    def validate_date(cls, value):
        from datetime import date
        date.fromisoformat(value)
        return value

def audit_invoices(input_file=None, output_file=None):
    input_file = Path(input_file or DATA / "invoices.csv")
    output_file = Path(output_file or OUTPUTS / "audit_report.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    valid, invalid = [], []
    with input_file.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                item = Invoice(**row)
                valid.append(item.model_dump())
            except Exception as exc:
                invalid.append({
                    "record": row,
                    "error": str(exc)
                })

    counts = Counter(x["invoice_id"] for x in valid)
    duplicates = [key for key, count in counts.items() if count > 1]
    total = round(sum(x["amount"] for x in valid), 2)

    report = {
        "total_records": len(valid) + len(invalid),
        "valid_invoices": len(valid),
        "invalid_invoices": len(invalid),
        "duplicate_invoice_ids": duplicates,
        "valid_amount_total": total,
        "currency_note": "Amounts are summed as supplied; mixed currencies are not converted.",
        "invalid_records": invalid,
        "audit_status": "completed"
    }

    output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
