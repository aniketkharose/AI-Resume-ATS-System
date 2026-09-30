from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcherError(Exception):
    """Base exception for semantic matching errors."""


# ============================================================
# TECHNICAL ABBREVIATION NORMALIZATION
# ============================================================

ABBREVIATION_MAP = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "api": "application programming interface",
    "apis": "application programming interface",
    "rest api": "rest application programming interface",
    "rest apis": "rest application programming interface",
    "llm": "large language model",
    "llms": "large language model",
    "genai": "generative artificial intelligence",
    "gen ai": "generative artificial intelligence",
    "rag": "retrieval augmented generation",
    "sql": "structured query language",
    "db": "database",
    "dbms": "database management system",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "k8s": "kubernetes",
}


# ============================================================
# RELATED TECHNICAL SKILLS
# ============================================================

RELATED_SKILLS = {
    "machine learning": {
        "ml",
        "machine learning",
        "scikit learn",
        "scikit-learn",
    },
    "deep learning": {
        "deep learning",
        "neural networks",
        "neural network",
        "cnn",
        "rnn",
        "lstm",
    },
    "natural language processing": {
        "nlp",
        "natural language processing",
        "text processing",
        "language processing",
    },
    "computer vision": {
        "cv",
        "computer vision",
        "image processing",
        "opencv",
    },
    "generative ai": {
        "generative ai",
        "genai",
        "generative artificial intelligence",
        "llm",
        "llms",
        "large language model",
    },
    "retrieval augmented generation": {
        "rag",
        "retrieval augmented generation",
    },
    "python": {
        "python",
        "python programming",
    },
    "javascript": {
        "javascript",
        "js",
    },
    "application programming interface": {
        "api",
        "apis",
        "rest api",
        "rest apis",
        "application programming interface",
    },
    "database": {
        "database",
        "db",
        "sql",
    },
    "database management system": {
        "database management system",
        "dbms",
    },
    "amazon web services": {
        "aws",
        "amazon web services",
    },
    "google cloud platform": {
        "gcp",
        "google cloud platform",
    },
}


def _clean_text(text: str) -> str:
    """
    Normalize text before similarity calculation.
    """

    if not text:
        return ""

    text = str(text).strip().lower()

    # Normalize common separators.
    text = text.replace("_", " ")
    text = text.replace("-", " ")

    # Collapse repeated spaces.
    text = " ".join(text.split())

    return text


def _expanded_text(text: str) -> str:
    """
    Expand common technical abbreviations.

    Example:
        NLP -> natural language processing
        ML  -> machine learning
    """

    cleaned = _clean_text(text)

    if not cleaned:
        return ""

    words = cleaned.split()

    expanded_parts = []

    for word in words:
        expanded_parts.append(word)

        if word in ABBREVIATION_MAP:
            expanded_parts.append(
                ABBREVIATION_MAP[word]
            )

    return " ".join(expanded_parts)


def _canonical_relation(text: str) -> set[str]:
    """
    Return the related-skill group for a technical skill.
    """

    cleaned = _clean_text(text)

    if not cleaned:
        return set()

    related = set()

    for canonical, variants in RELATED_SKILLS.items():

        normalized_variants = {
            _clean_text(item)
            for item in variants
        }

        if cleaned in normalized_variants:
            related.update(normalized_variants)

    return related


def _lexical_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Lightweight similarity using word + character TF-IDF.

    This avoids loading PyTorch or a transformer model.
    """

    if not text_a or not text_b:
        return 0.0

    try:

        vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            lowercase=True,
        )

        vectors = vectorizer.fit_transform(
            [text_a, text_b]
        )

        score = cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]

        return float(
            max(
                0.0,
                min(1.0, score),
            )
        )

    except Exception as error:

        raise SemanticMatcherError(
            "Lightweight similarity calculation failed."
        ) from error


class SemanticMatcher:
    """
    Lightweight semantic-style matcher.

    This implementation intentionally avoids
    SentenceTransformer/PyTorch so it can run within
    low-memory deployment environments such as
    Render's 512 MB free instance.

    Matching strategy:

        1. Exact normalized text
        2. Technical abbreviation expansion
        3. Known technical relationship
        4. Character-level TF-IDF similarity
    """

    def __init__(self):
        pass

    # ========================================================
    # SINGLE TEXT SIMILARITY
    # ========================================================

    def calculate_similarity(
        self,
        text_a: str,
        text_b: str,
    ) -> float:
        """
        Calculate lightweight similarity between two skills/texts.

        Returns a value between 0 and 1.
        """

        if not text_a or not text_b:
            return 0.0

        original_a = _clean_text(text_a)
        original_b = _clean_text(text_b)

        # ----------------------------------------------------
        # 1. Exact match
        # ----------------------------------------------------

        if original_a == original_b:
            return 1.0

        # ----------------------------------------------------
        # 2. Expanded abbreviation match
        # ----------------------------------------------------

        expanded_a = _expanded_text(original_a)
        expanded_b = _expanded_text(original_b)

        if expanded_a == expanded_b:
            return 0.98

        # ----------------------------------------------------
        # 3. Known technical relationship
        # ----------------------------------------------------

        relation_a = _canonical_relation(original_a)
        relation_b = _canonical_relation(original_b)

        if relation_a and relation_b:
            if relation_a.intersection(relation_b):
                return 0.90

        # ----------------------------------------------------
        # 4. Lightweight character similarity
        # ----------------------------------------------------

        lexical_score = _lexical_similarity(
            expanded_a,
            expanded_b,
        )

        return round(
            lexical_score,
            4,
        )

    # ========================================================
    # SKILL COMPARISON
    # ========================================================

    def compare_skills(
        self,
        resume_skills: list[dict],
        jd_skills: list[dict],
        threshold: float = 0.65,
    ) -> list[dict[str, Any]]:
        """
        Compare JD skills against resume skills.

        Exact matching is handled by HybridMatcher.
        This method identifies lightweight semantic/
        related relationships.
        """

        if not resume_skills:
            return []

        if not jd_skills:
            return []

        resume_names = [
            item.get("skill", "")
            for item in resume_skills
            if item.get("skill")
        ]

        if not resume_names:
            return []

        results = []

        for jd_skill in jd_skills:

            jd_name = jd_skill.get(
                "skill",
                "",
            )

            if not jd_name:
                continue

            best_similarity = 0.0
            best_resume_skill = None

            for resume_skill in resume_skills:

                resume_name = resume_skill.get(
                    "skill",
                    "",
                )

                if not resume_name:
                    continue

                similarity = self.calculate_similarity(
                    jd_name,
                    resume_name,
                )

                if similarity > best_similarity:

                    best_similarity = similarity
                    best_resume_skill = resume_skill

            results.append(
                {
                    "jd_skill": jd_name,
                    "jd_category": jd_skill.get(
                        "category",
                        "Unknown",
                    ),
                    "importance": jd_skill.get(
                        "importance",
                        "general",
                    ),
                    "related_resume_skill": (
                        best_resume_skill.get("skill")
                        if best_resume_skill
                        else None
                    ),
                    "similarity": round(
                        best_similarity,
                        4,
                    ),
                    "semantic_match": (
                        best_similarity >= threshold
                    ),
                }
            )

        return results


# ============================================================
# SHARED MATCHER
# ============================================================

_default_matcher = SemanticMatcher()


def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Convenience function for lightweight similarity.
    """

    return _default_matcher.calculate_similarity(
        text_a,
        text_b,
    )