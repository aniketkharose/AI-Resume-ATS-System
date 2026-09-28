from typing import Any

from sklearn.metrics.pairwise import cosine_similarity

from backend.core.config import SENTENCE_TRANSFORMER_MODEL


class SemanticMatcherError(Exception):
    """Base exception for semantic matching errors."""


class SemanticMatcher:
    """
    Memory-optimized semantic matcher.

    The Sentence Transformer model is loaded lazily:
    it is NOT loaded when the FastAPI application starts.

    The model is loaded only when semantic matching is actually required.
    """

    def __init__(self):
        self.model = None

    def _get_model(self):
        """
        Lazily load the Sentence Transformer model.

        This prevents PyTorch + Sentence Transformer from consuming
        memory during FastAPI startup.
        """

        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer

                self.model = SentenceTransformer(
                    SENTENCE_TRANSFORMER_MODEL,
                    device="cpu",
                )

            except Exception as error:
                raise SemanticMatcherError(
                    "Failed to load the Sentence Transformer model."
                ) from error

        return self.model

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

        model = self._get_model()

        embeddings = model.encode(
            [text_a, text_b],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        # Since embeddings are normalized,
        # cosine similarity is simply their dot product.
        similarity = float(
            embeddings[0] @ embeddings[1]
        )

        similarity = max(
            0.0,
            min(1.0, similarity),
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
        This method discovers semantic relationships
        between skills.
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

        model = self._get_model()

        # Generate embeddings once.
        resume_embeddings = model.encode(
            resume_names,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        jd_embeddings = model.encode(
            jd_names,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        # Because embeddings are normalized,
        # matrix multiplication gives cosine similarity.
        similarity_matrix = (
            jd_embeddings @ resume_embeddings.T
        )

        results = []

        for jd_index, jd_skill in enumerate(jd_skills):

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


# One shared matcher instance.
# The actual ML model is still loaded lazily.
_default_matcher = SemanticMatcher()


def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Convenience function for comparing two texts.

    Uses one shared SemanticMatcher instance instead
    of creating/loading a new matcher every time.
    """

    return _default_matcher.calculate_similarity(
        text_a,
        text_b,
    )