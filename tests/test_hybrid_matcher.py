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


def test_hybrid_matcher():

    # ========================================================
    # RESUME
    # ========================================================

    resume_path = Path(
        "tests/sample_resume.pdf"
    )

    file_data = resume_path.read_bytes()

    resume_text, _ = parse_resume_file(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
    )

    nlp_result = process_resume_text(
        resume_text
    )

    resume_skills = (
        extract_skills_from_sections(
            nlp_result["sections"]
        )
    )

    # ========================================================
    # JOB DESCRIPTION
    # ========================================================

    jd_result = process_job_description(
        SAMPLE_JD,
        SKILL_DATABASE,
    )

    # ========================================================
    # HYBRID MATCHING
    # ========================================================

    matcher = HybridMatcher(
        semantic_threshold=0.65,
        related_threshold=0.45,
    )

    result = matcher.match(
        resume_skills=resume_skills,
        jd_skills=jd_result["skills"],
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print(
        "\n========== HYBRID MATCHING =========="
    )

    print("\nAll Results:\n")

    for item in result["results"]:

        status_icon = {
            "matched": "✅",
            "related": "⚠️",
            "missing": "❌",
        }.get(
            item["status"],
            "?"
        )

        print(
            f"{status_icon} "
            f"{item['jd_skill']}"
            f" | {item['status']}"
            f" | type: {item['match_type']}"
            f" | similarity: {item['similarity']}"
        )

        if item["resume_skill"]:

            print(
                f"   Resume skill: "
                f"{item['resume_skill']}"
            )

        if item["resume_evidence"]:

            print(
                f"   Evidence: "
                f"{item['resume_evidence']}"
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n========== SUMMARY =========="
    )

    stats = result["statistics"]

    print(
        "Total:",
        stats["total"],
    )

    print(
        "Matched:",
        stats["matched"],
    )

    print(
        "Related:",
        stats["related"],
    )

    print(
        "Missing:",
        stats["missing"],
    )

    print(
        "Required Match:",
        stats[
            "required_match_percentage"
        ],
        "%",
    )

    print(
        "Preferred Match:",
        stats[
            "preferred_match_percentage"
        ],
        "%",
    )

    print(
        "\n========== MATCHED =========="
    )

    for item in result["matched"]:
        print(
            f"✅ {item['jd_skill']}"
            f" → {item['match_type']}"
        )

    print(
        "\n========== RELATED =========="
    )

    for item in result["related"]:
        print(
            f"⚠️ {item['jd_skill']}"
            f" → {item['resume_skill']}"
            f" ({item['similarity']})"
        )

    print(
        "\n========== MISSING =========="
    )

    for item in result["missing"]:
        print(
            f"❌ {item['jd_skill']}"
            f" ({item['similarity']})"
        )

    print(
        "\n✅ Hybrid matcher working successfully."
    )


if __name__ == "__main__":
    test_hybrid_matcher()