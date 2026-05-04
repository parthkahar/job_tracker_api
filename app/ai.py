def build_followup_prompt(company_name: str, job_title: str, status: str, notes: str) -> str:
    prompt = f"""
Write a professional follow-up message for a job application.

Company: {company_name}
Role: {job_title}
Current Status: {status}
Notes: {notes}

Keep the message polite, short and professional.
"""
    return prompt.strip()


def generate_followup(company_name: str, job_title: str, status: str, notes: str) -> str:
    prompt = build_followup_prompt(company_name, job_title, status, notes)

    followup_text = f"""
Hey, here is the follow-up for {company_name} and {job_title}.

Status: {status}
Notes: {notes}

Prompt created successfully:
{prompt}
"""
    return followup_text.strip()