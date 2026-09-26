from pathlib import Path

from backend.services.resume_analyzer import (
    analyze_resume,
)


def test_resume_analyzer():

    resume_path = Path(
        "tests/sample_resume.pdf"
    )

    file_data = resume_path.read_bytes()

    result = analyze_resume(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
        use_groq=True,
    )

    print(
        "\n========== UNIFIED RESUME ANALYSIS =========="
    )

    print(
        "\nFile:",
        result["metadata"]["filename"],
    )

    print(
        "Extracted characters:",
        result["metadata"]["text_length"],
    )

    print(
        "\nNLP:"
    )

    print(
        "Tokens:",
        result["nlp"]["token_count"],
    )

    print(
        "Sentences:",
        result["nlp"]["sentence_count"],
    )

    print(
        "\nDetected Skills:"
    )

    for skill in result["skills"]:

        print(
            f"✅ {skill['skill']}"
            f" → {skill['category']}"
            f" | {skill['source']}"
        )

    groq = result["groq"]

    print(
        "\n========== GROQ STATUS =========="
    )

    print(
        "Enabled:",
        groq["enabled"],
    )

    print(
        "Success:",
        groq["success"],
    )

    if groq["error"]:

        print(
            "Error:",
            groq["error"],
        )

    if groq["data"]:

        print(
            "\nGroq Projects:"
        )

        for project in groq["data"].get(
            "projects",
            [],
        ):

            print(
                f"🚀 {project['name']}"
            )

            print(
                "   Technologies:",
                ", ".join(
                    project["technologies"]
                ),
            )

    print(
        "\n✅ Unified resume analysis completed."
    )


if __name__ == "__main__":
    test_resume_analyzer()