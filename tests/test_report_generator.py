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

from backend.services.recommendation_engine import (
    generate_recommendations,
)

from backend.services.report_generator import (
    generate_ats_report,
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


def test_report_generator():

    # ========================================================
    # RESUME
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
    # NLP
    # ========================================================

    nlp_result = process_resume_text(
        resume_text
    )

    # ========================================================
    # SKILLS
    # ========================================================

    resume_skills = (
        extract_skills_from_sections(
            nlp_result["sections"]
        )
    )

    # ========================================================
    # RESUME ANALYSIS
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
    # JD
    # ========================================================

    jd_result = (
        process_job_description(
            SAMPLE_JD,
            SKILL_DATABASE,
        )
    )

    # ========================================================
    # HYBRID MATCHING
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
    # ATS
    # ========================================================

    ats_result = calculate_ats_score(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
    )

    # ========================================================
    # FEEDBACK
    # ========================================================

    feedback = generate_feedback(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
        ats_result=ats_result,
    )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = generate_recommendations(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
        ats_result=ats_result,
        feedback=feedback,
    )

    # ========================================================
    # PDF
    # ========================================================

    output_path = Path(
        "tests/test_ats_report.pdf"
    )

    generated_file = generate_ats_report(
        output_path=output_path,
        ats_result=ats_result,
        feedback=feedback,
        recommendations=recommendations,
        filename=resume_path.name,
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    assert Path(
        generated_file
    ).exists()

    assert Path(
        generated_file
    ).stat().st_size > 0

    print(
        "\n========== PDF REPORT GENERATOR =========="
    )

    print(
        "\nGenerated:",
        generated_file,
    )

    print(
        "File size:",
        Path(
            generated_file
        ).stat().st_size,
        "bytes",
    )

    print(
        "\nATS Score:",
        ats_result["ats_score"],
    )

    print(
        "\n✅ PDF report generator working successfully."
    )


if __name__ == "__main__":
    test_report_generator()