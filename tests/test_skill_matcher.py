from pathlib import Path

from backend.services.resume_parser import (
    parse_resume_file,
)

from backend.services.nlp_processor import (
    process_resume_text,
)

from backend.services.skill_extractor import (
    extract_skills_from_sections,
)

from backend.services.jd_parser import (
    process_job_description,
)

from backend.services.skill_matcher import (
    match_jd_skills,
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


def test_skill_matcher():

    # ========================================================
    # STEP 1: LOAD RESUME
    # ========================================================

    resume_path = Path(
        "tests/sample_resume.pdf"
    )

    if not resume_path.exists():
        print(
            "❌ sample_resume.pdf not found."
        )
        return

    file_data = resume_path.read_bytes()

    resume_text, _ = parse_resume_file(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
    )

    # ========================================================
    # STEP 2: RESUME NLP
    # ========================================================

    nlp_result = process_resume_text(
        resume_text
    )

    # ========================================================
    # STEP 3: RESUME SKILLS
    # ========================================================

    resume_skills = extract_skills_from_sections(
        nlp_result["sections"]
    )

    # ========================================================
    # STEP 4: PROCESS JD
    # ========================================================

    jd_result = process_job_description(
        SAMPLE_JD,
        __import__(
            "backend.services.skill_extractor",
            fromlist=["SKILL_DATABASE"],
        ).SKILL_DATABASE,
    )

    # ========================================================
    # STEP 5: MATCH
    # ========================================================

    result = match_jd_skills(
        resume_skills=resume_skills,
        jd_skills=jd_result["skills"],
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print(
        "\n========== EXACT SKILL MATCHING =========="
    )

    print(
        "\nRequired Match:",
        result[
            "required_match_percentage"
        ],
        "%",
    )

    print(
        "Preferred Match:",
        result[
            "preferred_match_percentage"
        ],
        "%",
    )

    print(
        "Overall Match:",
        result[
            "overall_match_percentage"
        ],
        "%",
    )

    print(
        "\n========== MATCHED REQUIRED =========="
    )

    for item in result[
        "matched_required"
    ]:

        print(
            f"✅ {item['skill']}"
            f" | Resume source: "
            f"{item['resume_source']}"
            f" | Evidence: "
            f"{item['resume_evidence']}"
        )

    print(
        "\n========== MISSING REQUIRED =========="
    )

    for item in result[
        "missing_required"
    ]:

        print(
            f"❌ {item['skill']}"
            f" | Category: "
            f"{item['category']}"
        )

    print(
        "\n========== MATCHED PREFERRED =========="
    )

    for item in result[
        "matched_preferred"
    ]:

        print(
            f"✅ {item['skill']}"
        )

    print(
        "\n========== MISSING PREFERRED =========="
    )

    for item in result[
        "missing_preferred"
    ]:

        print(
            f"⚠️ {item['skill']}"
        )

    print(
        "\n========== STATISTICS =========="
    )

    for key, value in result[
        "statistics"
    ].items():

        print(
            f"{key}: {value}"
        )

    print(
        "\n✅ Exact skill matching working successfully."
    )


if __name__ == "__main__":
    test_skill_matcher()