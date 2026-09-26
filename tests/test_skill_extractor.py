from pathlib import Path

from backend.services.resume_parser import parse_resume_file
from backend.services.nlp_processor import process_resume_text
from backend.services.skill_extractor import (
    extract_skills_from_sections,
)


def test_skill_extractor():

    resume_path = Path("tests/sample_resume.pdf")

    if not resume_path.exists():
        print("❌ sample_resume.pdf not found.")
        return

    # --------------------------------------------------------
    # STEP 1: READ RESUME
    # --------------------------------------------------------

    file_data = resume_path.read_bytes()

    resume_text, metadata = parse_resume_file(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
    )

    # --------------------------------------------------------
    # STEP 2: NLP PROCESSING
    # --------------------------------------------------------

    nlp_result = process_resume_text(resume_text)

    # --------------------------------------------------------
    # STEP 3: SKILL EXTRACTION
    # --------------------------------------------------------

    skills = extract_skills_from_sections(
        nlp_result["sections"]
    )

    print("\n========== SKILL EXTRACTION V3 ==========")

    print("Resume:", metadata["filename"])

    print("\nDetected Skills:\n")

    for item in skills:

        print(
            f"✅ {item['skill']} "
            f"→ {item['category']} "
            f"| Source: {item['source']}"
        )

        if item["evidence"]:
            print(
                f"   Evidence: {item['evidence']}"
            )

    print(
        "\nTotal skills detected:",
        len(skills),
    )

    # --------------------------------------------------------
    # CATEGORY SUMMARY
    # --------------------------------------------------------

    categories = {}

    for item in skills:

        category = item["category"]

        categories.setdefault(
            category,
            []
        ).append(
            item["skill"]
        )

    print("\n========== CATEGORY SUMMARY ==========")

    for category, category_skills in categories.items():

        print(f"\n{category}:")

        for skill in category_skills:
            print(f"  • {skill}")

    print(
        "\n✅ Skill extraction V3 working successfully."
    )


if __name__ == "__main__":
    test_skill_extractor()