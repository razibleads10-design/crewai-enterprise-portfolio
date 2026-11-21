
import unittest
import tempfile
import csv
import json

from pathlib import Path
from src.lead_pipeline import score_lead, process_leads
from src.invoice_audit import audit_invoices


class EnterpriseExtendedTests(unittest.TestCase):

    def test_empty_lead_fields_score_zero(self):
        self.assertEqual(score_lead({}), 0)

    def test_invalid_employee_count(self):
        row = {
            "company": "Example Ltd",
            "email": "info@example.test",
            "website": "",
            "industry": "Technology",
            "employees": "unknown"
        }
        self.assertEqual(score_lead(row), 60)

    def test_lead_processing_creates_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "leads.csv"
            output = Path(tmp) / "result.csv"

            with source.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["company", "email", "website",
                                "industry", "employees"]
                )
                writer.writeheader()
                writer.writerow({
                    "company": "Demo Ltd",
                    "email": "demo@example.test",
                    "website": "https://example.test",
                    "industry": "IT",
                    "employees": "100"
                })

            result = process_leads(source, output)

            self.assertEqual(result["total_leads"], 1)
            self.assertTrue(output.exists())

            with output.open(encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["lead_score"], "100")
            self.assertEqual(rows[0]["lead_category"], "High")

    def test_invoice_invalid_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "invoices.csv"
            output = Path(tmp) / "report.json"

            source.write_text(
                "invoice_id,vendor,amount,currency,invoice_date\n"
                "A1,Vendor A,100,USD,invalid-date\n",
                encoding="utf-8"
            )

            report = audit_invoices(source, output)

            self.assertEqual(report["valid_invoices"], 0)
            self.assertEqual(report["invalid_invoices"], 1)
            self.assertTrue(output.exists())

    def test_invoice_blank_vendor(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "invoices.csv"
            output = Path(tmp) / "report.json"

            source.write_text(
                "invoice_id,vendor,amount,currency,invoice_date\n"
                "A1,,100,USD,2026-01-01\n",
                encoding="utf-8"
            )

            report = audit_invoices(source, output)

            self.assertEqual(report["invalid_invoices"], 1)

    def test_invoice_empty_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "invoices.csv"
            output = Path(tmp) / "report.json"

            source.write_text(
                "invoice_id,vendor,amount,currency,invoice_date\n",
                encoding="utf-8"
            )

            report = audit_invoices(source, output)

            self.assertEqual(report["total_records"], 0)
            self.assertEqual(report["valid_invoices"], 0)
            self.assertEqual(report["invalid_invoices"], 0)

            saved = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(saved["audit_status"], "completed")


if __name__ == "__main__":
    unittest.main()
