import requests


# FastAPI backend URL
API_BASE_URL = "http://127.0.0.1:8000"


def analyze_resume(
    resume_file,
    job_description: str,
    use_groq: bool = True,
) -> dict:
    """
    Send resume + job description to the FastAPI ATS analysis endpoint.
    """

    if resume_file is None:
        raise ValueError("Resume file is required.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description is required.")

    files = {
        "resume": (
            resume_file.name,
            resume_file.getvalue(),
            resume_file.type,
        )
    }

    data = {
        "job_description": job_description.strip(),
        "use_groq": str(use_groq).lower(),
    }

    response = requests.post(
        f"{API_BASE_URL}/analysis/analyze",
        files=files,
        data=data,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()