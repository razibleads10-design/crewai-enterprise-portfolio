import unittest
import tempfile
from pathlib import Path
from src.lead_pipeline import score_lead, process_leads
from src.invoice_audit import audit_invoices

class PipelineTests(unittest.TestCase):
    def test_lead_scoring(self):
        row = {
            "company": "Example Ltd",
            "email": "info@example.test",
            "website": "https://example.test",
            "industry": "Technology",
            "employees": "100"
        }
        self.assertEqual(score_lead(row), 100)

    def test_invoice_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "invoices.csv"
            output = root / "report.json"
            source.write_text(
                "invoice_id,vendor,amount,currency,invoice_date\n"
                "A1,Vendor A,100,USD,2026-01-01\n"
                "A1,Vendor A,100,USD,2026-01-01\n"
                "A2,Vendor B,0,USD,2026-01-02\n",
                encoding="utf-8"
            )
            report = audit_invoices(source, output)
            self.assertEqual(report["valid_invoices"], 2)
            self.assertEqual(report["invalid_invoices"], 1)
            self.assertEqual(report["duplicate_invoice_ids"], ["A1"])
            self.assertTrue(output.exists())

if __name__ == "__main__":
    unittest.main()
