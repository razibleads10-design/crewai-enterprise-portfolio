import os

def build_agents():
    """Create CrewAI agents using Gemini when configured."""
    from crewai import Agent, LLM

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY before running CrewAI.")

    llm = LLM(
        model="gemini/gemini-3.5-flash-lite",
        api_key=api_key
    )

    researcher = Agent(
        role="B2B Lead Research Analyst",
        goal="Review supplied lead records and summarize their business relevance.",
        backstory="You are a careful B2B research analyst. Use only supplied data.",
        llm=llm,
        verbose=False
    )

    validator = Agent(
        role="Lead Data Quality Validator",
        goal="Identify missing, inconsistent or questionable lead fields.",
        backstory="You focus on structured data quality and avoid unsupported claims.",
        llm=llm,
        verbose=False
    )

    scorer = Agent(
        role="Lead Qualification Analyst",
        goal="Recommend lead priority using only the supplied record information.",
        backstory="You provide transparent, evidence-based lead prioritization.",
        llm=llm,
        verbose=False
    )

    return researcher, validator, scorer
