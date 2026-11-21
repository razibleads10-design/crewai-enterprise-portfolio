import csv
from pathlib import Path
from crewai import Crew, Process
from src.agents import build_agents
from src.tasks import create_tasks

ROOT = Path(__file__).resolve().parents[1]

def run_crew():
    data_file = ROOT / "data" / "leads.csv"
    with data_file.open("r", encoding="utf-8", newline="") as f:
        leads = list(csv.DictReader(f))

    agents = build_agents()
    tasks = create_tasks(*agents, lead_data=leads)

    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,
        verbose=False
    )
    result = crew.kickoff()
    output = ROOT / "outputs" / "crewai_analysis.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(str(result), encoding="utf-8")
    print("CrewAI execution completed:", output)
    return str(result)

if __name__ == "__main__":
    run_crew()
