from pathlib import Path

from backend.services.resume_parser import parse_resume_file
from backend.services.nlp_processor import process_resume_text
from backend.services.skill_extractor import extract_skills_from_sections


def test_skill_extractor():

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
    # STEP 2: NLP + sections
    # -----------------------------

    nlp_result = process_resume_text(resume_text)

    # -----------------------------
    # STEP 3: Extract skills
    # -----------------------------

    skills = extract_skills_from_sections(
        nlp_result["sections"]
    )

    print("\n========== SKILL EXTRACTION TEST ==========")

    print("Resume:", metadata["filename"])

    print("\nDetected Skills:")

    for skill in skills:
        print(f"✅ {skill}")

    print("\nTotal skills detected:", len(skills))

    print("\n✅ Skill extraction working successfully.")


if __name__ == "__main__":
    test_skill_extractor()