from crewai import Task

def create_tasks(researcher, validator, scorer, lead_data):
    research_task = Task(
        description=(
            "Review these fictional B2B lead records. Summarize each company's "
            "industry, available contact fields and potential relevance. "
            "Do not invent facts. Data: " + str(lead_data)
        ),
        expected_output="A concise structured summary based only on supplied data.",
        agent=researcher
    )

    validation_task = Task(
        description=(
            "Review the supplied lead records for missing or inconsistent fields. "
            "Do not attempt to contact anyone or claim external verification. "
            "Data: " + str(lead_data)
        ),
        expected_output="A list of data quality observations and missing fields.",
        agent=validator,
        context=[research_task]
    )

    scoring_task = Task(
        description=(
            "Prioritize the supplied leads using only available evidence. "
            "Explain the factors behind each priority. Data: " + str(lead_data)
        ),
        expected_output="A prioritized lead summary with transparent reasoning.",
        agent=scorer,
        context=[research_task, validation_task]
    )

    return [research_task, validation_task, scoring_task]
