import requests

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

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Error: Unable to generate follow-up"