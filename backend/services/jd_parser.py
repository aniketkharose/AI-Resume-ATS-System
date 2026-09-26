import re


class JDParserError(Exception):
    """Base exception for Job Description parsing errors."""


# ============================================================
# COMMON JOB-DESCRIPTION SECTION HEADINGS
# ============================================================

SECTION_PATTERNS = {
    "requirements": [
        "requirements",
        "job requirements",
        "required skills",
        "required qualifications",
        "qualifications",
        "must have",
        "must-have",
    ],
    "preferred": [
        "preferred qualifications",
        "preferred skills",
        "nice to have",
        "nice-to-have",
        "good to have",
        "bonus skills",
    ],
    "responsibilities": [
        "responsibilities",
        "roles and responsibilities",
        "what you will do",
        "key responsibilities",
        "job responsibilities",
    ],
    "description": [
        "job description",
        "about the role",
        "role description",
        "about the job",
    ],
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_jd_text(text: str) -> str:
    """
    Clean Job Description text before processing.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize bullets
    text = re.sub(
        r"^[•●▪❖➢➤►]+",
        "-",
        text,
        flags=re.MULTILINE,
    )

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# SECTION DETECTION
# ============================================================

def detect_jd_sections(text: str) -> dict:
    """
    Detect common sections in a Job Description.
    """

    sections = {}

    current_section = "description"
    current_content = []

    normalized_text = normalize_jd_text(text)

    for line in normalized_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        normalized_line = line.lower()

        # Remove bullet characters
        normalized_line = re.sub(
            r"^[\-•●▪❖➢➤►\s]+",
            "",
            normalized_line,
        ).strip()

        matched_section = None

        for section_name, headings in SECTION_PATTERNS.items():

            if normalized_line in headings:
                matched_section = section_name
                break

        if matched_section:

            if current_content:
                sections[current_section] = "\n".join(
                    current_content
                ).strip()

            current_section = matched_section
            current_content = []

        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = "\n".join(
            current_content
        ).strip()

    return sections


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_jd_skills(
    text: str,
    skill_database: dict,
) -> list[dict]:
    """
    Extract skills from a Job Description using the same
    domain-aware skill database used by the resume extractor.
    """

    if not text:
        return []

    normalized_text = normalize_jd_text(text).lower()

    detected_skills = []
    detected_names = set()

    for category, skills in skill_database.items():

        for canonical_skill, aliases in skills.items():

            matched_alias = None

            for alias in aliases:

                normalized_alias = alias.lower().strip()

                escaped_alias = re.escape(
                    normalized_alias
                )

                pattern = (
                    rf"(?<![a-z0-9+#])"
                    rf"{escaped_alias}"
                    rf"(?![a-z0-9+#])"
                )

                if re.search(
                    pattern,
                    normalized_text,
                ):
                    matched_alias = alias
                    break

            if not matched_alias:
                continue

            if canonical_skill in detected_names:
                continue

            detected_skills.append(
                {
                    "skill": canonical_skill,
                    "category": category,
                    "matched_alias": matched_alias,
                }
            )

            detected_names.add(canonical_skill)

    return detected_skills


# ============================================================
# REQUIRED vs PREFERRED
# ============================================================

def classify_jd_skills(
    skills: list[dict],
    sections: dict,
) -> list[dict]:
    """
    Classify detected skills as required, preferred,
    or general based on the section where they appear.
    """

    required_text = sections.get(
        "requirements",
        "",
    ).lower()

    preferred_text = sections.get(
        "preferred",
        "",
    ).lower()

    classified_skills = []

    for skill in skills:

        alias = skill["matched_alias"].lower()

        if alias in required_text:

            importance = "required"

        elif alias in preferred_text:

            importance = "preferred"

        else:

            importance = "general"

        classified_skills.append(
            {
                **skill,
                "importance": importance,
            }
        )

    return classified_skills


# ============================================================
# MAIN JD PROCESSOR
# ============================================================

def process_job_description(
    text: str,
    skill_database: dict,
) -> dict:
    """
    Complete Job Description processing pipeline.
    """

    if not text or not text.strip():
        raise JDParserError(
            "Job Description cannot be empty."
        )

    cleaned_text = normalize_jd_text(text)

    sections = detect_jd_sections(
        cleaned_text
    )

    skills = extract_jd_skills(
        cleaned_text,
        skill_database,
    )

    skills = classify_jd_skills(
        skills,
        sections,
    )

    return {
        "cleaned_text": cleaned_text,
        "sections": sections,
        "skills": skills,
        "skill_count": len(skills),
    }