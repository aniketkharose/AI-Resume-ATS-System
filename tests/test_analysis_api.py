from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


SAMPLE_JD = """
AI/ML Engineer

Requirements

- Strong Python programming skills
- Experience with Machine Learning and Deep Learning
- Knowledge of NLP and Transformers
- Experience with PyTorch or TensorFlow
- Knowledge of SQL
- Experience building REST APIs
- Git and GitHub knowledge

Preferred Qualifications

- Experience with Generative AI
- Knowledge of RAG
- Experience with FastAPI
- Experience with Docker
"""


def test_analysis_api():

    resume_path = "tests/sample_resume.pdf"

    with open(
        resume_path,
        "rb",
    ) as resume_file:

        response = client.post(
            "/analysis/analyze",
            files={
                "resume": (
                    "sample_resume.pdf",
                    resume_file,
                    "application/pdf",
                )
            },
            data={
                "job_description": SAMPLE_JD,
                "use_groq": "false",
            },
        )

    print(
        "\n========== ANALYSIS API =========="
    )

    print(
        "Status:",
        response.status_code,
    )

    assert response.status_code == 200

    result = response.json()

    print(
        "\nATS Score:",
        result["ats"]["ats_score"],
    )

    print(
        "\n========== JD IMPORTANCE =========="
    )

    for item in result[
        "job_description"
    ]["skills"]:

        print(
            f"{item['skill']} "
            f"→ {item['importance']}"
        )

    print(
        "\n========== MISSING SKILLS =========="
    )

    for item in result[
        "feedback"
    ]["missing_skills"]:

        print(
            f"{item['skill']} "
            f"→ {item['priority']}"
        )

    print(
        "\n✅ Analysis API working successfully."
    )


if __name__ == "__main__":
    test_analysis_api()