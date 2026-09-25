import re


# Skill vocabulary used by the ATS.
# We can expand this as the project grows.
SKILL_ALIASES = {
    "Python": ["python"],
    "C": [r"\bc\b"],
    "C++": ["c++"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "SQL": ["sql", "sq l"],

    "NumPy": ["numpy"],
    "Pandas": ["pandas"],
    "Matplotlib": ["matplotlib"],
    "Scikit-learn": ["scikit-learn", "scikit -learn", "sklearn"],

    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"],
    "Transformers": ["transformers", "transformer"],
    "LLMs": ["llm", "llms", "large language models"],
    "Generative AI": ["generative ai", "gen ai"],
    "RAG": ["rag", "retrieval augmented generation"],

    "PyTorch": ["pytorch"],
    "TensorFlow": ["tensorflow"],
    "Keras": ["keras"],

    "OpenAI": ["openai", "openai apis"],
    "FastAPI": ["fastapi", "fast api"],
    "Flask": ["flask"],

    "Git": ["git"],
    "GitHub": ["github"],

    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react"],

    "Streamlit": ["streamlit"],
    "OpenCV": ["opencv"],
    "MediaPipe": ["mediapipe"],
    "Dlib": ["dlib"],
    "SVM": ["svm"],

    "Supabase": ["supabase"],
    "SQLite": ["sqlite"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],

    "REST APIs": ["rest api", "rest apis"],
    "Flask": ["flask"],
}


def normalize_text(text: str) -> str:
    """
    Normalize text for skill matching.

    This does NOT modify the original resume.
    It only creates a matching-friendly version.
    """

    text = text.lower()

    # Fix common PDF extraction spacing artifacts.
    text = re.sub(r"\bsq\s+l\b", "sql", text)
    text = re.sub(r"\bfast\s+api\b", "fastapi", text)
    text = re.sub(r"\bscikit\s*-\s*learn\b", "scikit-learn", text)

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def skill_found(text: str, alias: str) -> bool:
    """
    Check whether a skill alias exists as a meaningful occurrence.
    """

    alias = alias.lower().strip()

    # Special handling for short technical terms.
    if alias in {"c", "c++"}:
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
    else:
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"

    return re.search(pattern, text) is not None


def extract_skills(text: str) -> list[str]:
    """
    Extract known skills from resume text.

    Returns canonical skill names.
    """

    if not text:
        return []

    normalized_text = normalize_text(text)

    detected_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if skill_found(normalized_text, alias):
                detected_skills.append(canonical_skill)
                break

    return detected_skills


def extract_skills_from_sections(sections: dict) -> list[str]:
    """
    Prefer the dedicated Skills section when available,
    while still checking the complete resume.
    """

    skills_text = sections.get("skills", "")

    all_section_text = "\n".join(
        sections.values()
    )

    combined_text = f"{skills_text}\n{all_section_text}"

    return extract_skills(combined_text)