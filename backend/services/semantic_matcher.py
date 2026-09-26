from typing import Any

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from backend.core.config import SENTENCE_TRANSFORMER_MODEL


class SemanticMatcherError(Exception):
    """Base exception for semantic matching errors."""


class SemanticMatcher:
    def __init__(self):
        try:
            self.model = SentenceTransformer(
                SENTENCE_TRANSFORMER_MODEL
            )
        except Exception as error:
            raise SemanticMatcherError(
                "Failed to load the Sentence Transformer model."
            ) from error

    def calculate_similarity(
        self,
        text_a: str,
        text_b: str,
    ) -> float:
        """
        Calculate cosine similarity between two pieces of text.
        Returns a value between 0 and 1.
        """

        if not text_a or not text_b:
            return 0.0

        embeddings = self.model.encode(
            [text_a, text_b],
            convert_to_numpy=True,
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]],
        )[0][0]

        # Numerical safety
        similarity = max(
            0.0,
            min(1.0, float(similarity)),
        )

        return round(similarity, 4)

    def compare_skills(
        self,
        resume_skills: list[dict],
        jd_skills: list[dict],
        threshold: float = 0.65,
    ) -> list[dict[str, Any]]:
        """
        Compare every JD skill against resume skills.

        Exact matching is handled separately.
        This method is intended to discover semantic
        relationships between skills.
        """

        if not resume_skills:
            return []

        if not jd_skills:
            return []

        resume_names = [
            item["skill"]
            for item in resume_skills
            if item.get("skill")
        ]

        jd_names = [
            item["skill"]
            for item in jd_skills
            if item.get("skill")
        ]

        if not resume_names or not jd_names:
            return []

        # Generate embeddings once instead of repeatedly.
        resume_embeddings = self.model.encode(
            resume_names,
            convert_to_numpy=True,
        )

        jd_embeddings = self.model.encode(
            jd_names,
            convert_to_numpy=True,
        )

        similarity_matrix = cosine_similarity(
            jd_embeddings,
            resume_embeddings,
        )

        results = []

        for jd_index, jd_skill in enumerate(
            jd_skills
        ):

            best_resume_index = similarity_matrix[
                jd_index
            ].argmax()

            similarity_score = float(
                similarity_matrix[
                    jd_index,
                    best_resume_index,
                ]
            )

            best_resume_skill = resume_skills[
                best_resume_index
            ]

            results.append(
                {
                    "jd_skill": jd_skill["skill"],
                    "jd_category": jd_skill.get(
                        "category",
                        "Unknown",
                    ),
                    "importance": jd_skill.get(
                        "importance",
                        "general",
                    ),
                    "related_resume_skill": (
                        best_resume_skill["skill"]
                    ),
                    "similarity": round(
                        similarity_score,
                        4,
                    ),
                    "semantic_match": (
                        similarity_score >= threshold
                    ),
                }
            )

        return results


def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Convenience function for comparing two texts.
    """

    matcher = SemanticMatcher()

    return matcher.calculate_similarity(
        text_a,
        text_b,
    )