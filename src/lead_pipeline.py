import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"

def score_lead(row):
    """Deterministic example scoring; not a real-world lead verification."""
    score = 0
    if row.get("company", "").strip():
        score += 20
    if row.get("email", "").strip():
        score += 25
    if row.get("website", "").strip():
        score += 15
    if row.get("industry", "").strip():
        score += 15
    try:
        employees = int(row.get("employees", 0))
    except (ValueError, TypeError):
        employees = 0
    if employees >= 50:
        score += 25
    return min(score, 100)

def process_leads(input_file=None, output_file=None):
    input_file = Path(input_file or DATA / "leads.csv")
    output_file = Path(output_file or OUTPUTS / "enriched_leads.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results = []
    with input_file.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["lead_score"] = score_lead(row)
            row["lead_category"] = (
                "High" if row["lead_score"] >= 75 else
                "Medium" if row["lead_score"] >= 45 else "Low"
            )
            row["processing_status"] = "processed"
            results.append(row)

    if results:
        with output_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            writer.writeheader()
            writer.writerows(results)

    return {
        "total_leads": len(results),
        "high": sum(x["lead_category"] == "High" for x in results),
        "medium": sum(x["lead_category"] == "Medium" for x in results),
        "low": sum(x["lead_category"] == "Low" for x in results),
        "output": str(output_file)
    }
