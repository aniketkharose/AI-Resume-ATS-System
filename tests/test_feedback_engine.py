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

from backend.services.feedback_engine import (
    generate_feedback,
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


def test_feedback_engine():

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
    # STEP 4: RESUME ANALYSIS
    # ========================================================

    resume_analysis = {

        "metadata": metadata,

        "raw_text": resume_text,

        "nlp": {

            "token_count":
                nlp_result["token_count"],

            "sentence_count":
                nlp_result["sentence_count"],

            "sections":
                nlp_result["sections"],
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

    ats_result = calculate_ats_score(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
    )

    # ========================================================
    # STEP 8: FEEDBACK
    # ========================================================

    feedback = generate_feedback(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
        ats_result=ats_result,
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print(
        "\n========== FEEDBACK ENGINE =========="
    )

    print(
        "\nSUMMARY:"
    )

    print(
        feedback["summary"]
    )

    print(
        "\n========== STRENGTHS =========="
    )

    for strength in feedback["strengths"]:

        print(
            f"✓ {strength}"
        )

    print(
        "\n========== MISSING SKILLS =========="
    )

    if feedback["missing_skills"]:

        for skill in feedback[
            "missing_skills"
        ]:

            print(
                f"✗ {skill['skill']} "
                f"({skill['priority']})"
            )

    else:

        print(
            "No missing skills."
        )

    print(
        "\n========== RELATED SKILLS =========="
    )

    if feedback["related_skills"]:

        for skill in feedback[
            "related_skills"
        ]:

            print(
                f"~ {skill['jd_skill']} "
                f"→ {skill['resume_skill']} "
                f"(similarity: "
                f"{skill['similarity']})"
            )

    else:

        print(
            "No related skills detected."
        )

    print(
        "\n========== IMPROVEMENTS =========="
    )

    for improvement in feedback[
        "improvements"
    ]:

        print(
            f"→ {improvement}"
        )

    print(
        "\n✅ Feedback engine working successfully."
    )


if __name__ == "__main__":
    test_feedback_engine()