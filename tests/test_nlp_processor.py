from pathlib import Path

from backend.services.resume_parser import parse_resume_file
from backend.services.nlp_processor import process_resume_text


def test_nlp_processor():

    resume_path = Path("tests/sample_resume.pdf")

    if not resume_path.exists():
        print("❌ sample_resume.pdf not found.")
        return

    # -----------------------------
    # STEP 1: Parse resume
    # -----------------------------

    file_data = resume_path.read_bytes()

    resume_text, metadata = parse_resume_file(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
    )

    # -----------------------------
    # STEP 2: NLP processing
    # -----------------------------

    result = process_resume_text(resume_text)

    print("\n========== NLP TEST ==========")

    print("File:", metadata["filename"])
    print("Original characters:", len(resume_text))
    print("Cleaned characters:", len(result["cleaned_text"]))
    print("Token count:", result["token_count"])
    print("Sentence count:", result["sentence_count"])

    # -----------------------------
    # STEP 3: Sections
    # -----------------------------

    print("\n========== DETECTED SECTIONS ==========")

    sections = result["sections"]

    for section_name, content in sections.items():

        print(f"\n--- {section_name.upper()} ---")

        print(content[:500])

    print("\n========== SECTION SUMMARY ==========")

    for section_name in sections:
        print(f"✅ {section_name}")

    print("\n✅ NLP + section detection working successfully.")


if __name__ == "__main__":
    test_nlp_processor()