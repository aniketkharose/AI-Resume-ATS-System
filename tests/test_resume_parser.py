from pathlib import Path

from backend.services.resume_parser import parse_resume_file

def test_pdf_parser():
    """
    Test PDF resume parsing.
    """

    resume_path = Path("tests/sample_resume.pdf")

    if not resume_path.exists():
        print("❌ sample_resume.pdf not found.")
        return

    file_data = resume_path.read_bytes()

    text, metadata = parse_resume_file(
        file_data=file_data,
        filename=resume_path.name,
        content_type="application/pdf",
    )

    print("\n========== PARSER TEST ==========")

    print("File:", metadata["filename"])
    print("Type:", metadata["file_type"])
    print("Size:", metadata["file_size_bytes"], "bytes")
    print("Extracted characters:", metadata["text_length"])

    print("\n---------- Extracted Text ----------")
    print(text[:2000])

    print("\n✅ PDF parser working successfully.")


if __name__ == "__main__":
    test_pdf_parser()