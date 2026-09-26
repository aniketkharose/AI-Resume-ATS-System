from typing import Any

from backend.services.resume_parser import (
    parse_resume_file,
)

from backend.services.nlp_processor import (
    process_resume_text,
)

from backend.services.skill_extractor import (
    extract_skills_from_sections,
)

from backend.services.groq_parser import (
    parse_resume_with_groq,
)


class ResumeAnalyzerError(Exception):
    """Base exception for resume analysis errors."""


def analyze_resume(
    file_data: bytes,
    filename: str,
    content_type: str | None = None,
    use_groq: bool = True,
) -> dict[str, Any]:
    """
    Complete resume analysis pipeline.

    Pipeline:
        File
        ↓
        Parser
        ↓
        NLP / Sections
        ↓
        Domain Skill Extraction
        ↓
        Optional Groq structured parsing
    """

    # ========================================================
    # STEP 1: FILE PARSING
    # ========================================================

    try:

        resume_text, metadata = parse_resume_file(
            file_data=file_data,
            filename=filename,
            content_type=content_type,
        )

    except Exception as error:

        raise ResumeAnalyzerError(
            f"Resume parsing failed: {error}"
        ) from error

    # ========================================================
    # STEP 2: NLP
    # ========================================================

    try:

        nlp_result = process_resume_text(
            resume_text
        )

    except Exception as error:

        raise ResumeAnalyzerError(
            f"NLP processing failed: {error}"
        ) from error

    # ========================================================
    # STEP 3: DOMAIN-AWARE SKILL EXTRACTION
    # ========================================================

    try:

        skills = extract_skills_from_sections(
            nlp_result["sections"]
        )

    except Exception as error:

        raise ResumeAnalyzerError(
            f"Skill extraction failed: {error}"
        ) from error

    # ========================================================
    # STEP 4: GROQ STRUCTURED PARSING
    # ========================================================

    groq_result = None
    groq_error = None

    if use_groq:

        try:

            groq_result = parse_resume_with_groq(
                resume_text
            )

        except Exception as error:

            # Groq should enhance the analysis,
            # but a temporary API failure should
            # not destroy the basic resume analysis.
            groq_error = str(error)

    # ========================================================
    # STEP 5: UNIFIED RESULT
    # ========================================================

    return {
        "metadata": metadata,

        "raw_text": resume_text,

        "nlp": {
            "token_count": nlp_result[
                "token_count"
            ],
            "sentence_count": nlp_result[
                "sentence_count"
            ],
            "entities": nlp_result[
                "entities"
            ],
            "sections": nlp_result[
                "sections"
            ],
        },

        "skills": skills,

        "groq": {
            "enabled": use_groq,
            "success": groq_result is not None,
            "data": groq_result,
            "error": groq_error,
        },
    }