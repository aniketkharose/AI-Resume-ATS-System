from pathlib import Path

from backend.services.resume_parser import (
    parse_resume_file,
)

from backend.services.groq_parser import (
    parse_resume_with_groq,
    GroqParserError,
)


def test_groq_parser():

    resume_path = Path(
        "tests/sample_resume.pdf"
    )

    if not resume_path.exists():
        print(
            "❌ sample_resume.pdf not found."
        )
        return

    # ========================================================
    # STEP 1: READ RESUME FILE
    # ========================================================

    file_data = resume_path.read_bytes()

    resume_text, metadata = parse_resume_file(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
    )

    print(
        "\n========== GROQ RESUME PARSER =========="
    )

    print(
        "Resume:",
        metadata["filename"],
    )

    print(
        "Characters:",
        metadata["text_length"],
    )

    # ========================================================
    # STEP 2: GROQ PARSING
    # ========================================================

    try:

        result = parse_resume_with_groq(
            resume_text
        )

    except GroqParserError as error:

        print(
            "\n❌ Groq parser failed:"
        )

        print(error)

        return

    # ========================================================
    # STEP 3: DISPLAY CONTACT
    # ========================================================

    print(
        "\n========== CONTACT =========="
    )

    contact = result.get(
        "contact",
        {},
    )

    for key, value in contact.items():

        print(
            f"{key}: {value}"
        )

    # ========================================================
    # STEP 4: SKILLS
    # ========================================================

    print(
        "\n========== SKILLS =========="
    )

    for skill in result.get(
        "skills",
        [],
    ):

        print(
            f"• {skill}"
        )

    # ========================================================
    # STEP 5: EDUCATION
    # ========================================================

    print(
        "\n========== EDUCATION =========="
    )

    for education in result.get(
        "education",
        [],
    ):

        print(
            f"🎓 {education['degree']}"
            f" | {education['institution']}"
        )

    # ========================================================
    # STEP 6: EXPERIENCE
    # ========================================================

    print(
        "\n========== EXPERIENCE =========="
    )

    for experience in result.get(
        "experience",
        [],
    ):

        print(
            f"💼 {experience['job_title']}"
            f" | {experience['company']}"
        )

    # ========================================================
    # STEP 7: PROJECTS
    # ========================================================

    print(
        "\n========== PROJECTS =========="
    )

    for project in result.get(
        "projects",
        [],
    ):

        print(
            f"🚀 {project['name']}"
        )

        print(
            f"   Technologies: "
            f"{', '.join(project['technologies'])}"
        )

    # ========================================================
    # STEP 8: CERTIFICATIONS
    # ========================================================

    print(
        "\n========== CERTIFICATIONS =========="
    )

    for certification in result.get(
        "certifications",
        [],
    ):

        print(
            f"📜 {certification}"
        )

    # ========================================================
    # STEP 9: ACHIEVEMENTS
    # ========================================================

    print(
        "\n========== ACHIEVEMENTS =========="
    )

    for achievement in result.get(
        "achievements",
        [],
    ):

        print(
            f"🏆 {achievement}"
        )

    print(
        "\n✅ Groq resume parsing completed."
    )


if __name__ == "__main__":
    test_groq_parser()