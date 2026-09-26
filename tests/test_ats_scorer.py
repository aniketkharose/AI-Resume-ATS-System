from pathlib import Path

from backend.services.resume_parser import (
    parse_resume_file,
)

from backend.services.nlp_processor import (
    process_resume_text,
)

from backend.services.skill_extractor import (
    extract_skills_from_sections,
    SKILL_DATABASE,
)

from backend.services.jd_parser import (
    process_job_description,
)

from backend.services.hybrid_matcher import (
    HybridMatcher,
)

from backend.services.ats_scorer import (
    calculate_ats_score,
)


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


def test_ats_scorer():

    # ========================================================
    # STEP 1: RESUME
    # ========================================================

    resume_path = Path(
        "tests/sample_resume.pdf"
    )

    file_data = resume_path.read_bytes()

    resume_text, metadata = (
        parse_resume_file(
            file_data=file_data,
            filename=resume_path.name,
            content_type="application/pdf",
        )
    )

    # ========================================================
    # STEP 2: NLP
    # ========================================================

    nlp_result = process_resume_text(
        resume_text
    )

    # ========================================================
    # STEP 3: SKILLS
    # ========================================================

    resume_skills = (
        extract_skills_from_sections(
            nlp_result["sections"]
        )
    )

    # ========================================================
    # STEP 4: RESUME ANALYSIS OBJECT
    # ========================================================

    resume_analysis = {
        "metadata": metadata,

        "raw_text": resume_text,

        "nlp": {
            "token_count": nlp_result[
                "token_count"
            ],
            "sentence_count": nlp_result[
                "sentence_count"
            ],
            "sections": nlp_result[
                "sections"
            ],
        },

        "skills": resume_skills,
    }

    # ========================================================
    # STEP 5: JD
    # ========================================================

    jd_result = (
        process_job_description(
            SAMPLE_JD,
            SKILL_DATABASE,
        )
    )

    # ========================================================
    # STEP 6: HYBRID MATCHING
    # ========================================================

    matcher = HybridMatcher(
        semantic_threshold=0.65,
        related_threshold=0.45,
    )

    hybrid_result = matcher.match(
        resume_skills=resume_skills,
        jd_skills=jd_result["skills"],
    )

    # ========================================================
    # STEP 7: ATS SCORE
    # ========================================================

    result = calculate_ats_score(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print(
        "\n========== ATS SCORING ENGINE =========="
    )

    print(
        "\nFINAL ATS SCORE:",
        result["ats_score"],
        "/ 100",
    )

    print(
        "\n========== COMPONENT SCORES =========="
    )

    for name, score in result[
        "components"
    ].items():

        print(
            f"{name}: {score}/100"
        )

    print(
        "\n========== WEIGHTS =========="
    )

    for name, weight in result[
        "weights"
    ].items():

        print(
            f"{name}: {weight}%"
        )

    print(
        "\n========== WEIGHTED CONTRIBUTION =========="
    )

    for name, contribution in result[
        "weighted_contribution"
    ].items():

        print(
            f"{name}: +{contribution}"
        )

    print(
        "\n✅ ATS scoring engine working successfully."
    )


if __name__ == "__main__":
    test_ats_scorer()
    