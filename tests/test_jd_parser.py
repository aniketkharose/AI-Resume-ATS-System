from backend.services.jd_parser import (
    process_job_description,
)

from backend.services.skill_extractor import (
    SKILL_DATABASE,
)


SAMPLE_JD = """
AI/ML Engineer

About the Role

We are looking for an AI/ML Engineer to build and deploy
machine learning applications.

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

Responsibilities

- Develop machine learning models
- Build AI-powered applications
- Work with engineering teams
- Deploy production-ready solutions
"""


def test_jd_parser():

    result = process_job_description(
        SAMPLE_JD,
        SKILL_DATABASE,
    )

    print("\n========== JD PARSER ==========")

    print(
        "\nTotal skills detected:",
        result["skill_count"],
    )

    print("\nDetected Skills:\n")

    for skill in result["skills"]:

        print(
            f"✅ {skill['skill']}"
            f" → {skill['category']}"
            f" | {skill['importance']}"
            f" | matched: {skill['matched_alias']}"
        )

    print("\n========== JD SECTIONS ==========")

    for section_name, content in result[
        "sections"
    ].items():

        print(f"\n[{section_name.upper()}]")
        print(content[:300])

    print(
        "\n✅ JD parser working successfully."
    )


if __name__ == "__main__":
    test_jd_parser()