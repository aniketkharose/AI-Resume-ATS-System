from typing import Any

from backend.services.skill_matcher import (
    normalize_skill_name,
)

from backend.services.semantic_matcher import (
    SemanticMatcher,
)



class HybridMatcherError(Exception):
    """Base exception for hybrid matching errors."""


class HybridMatcher:
    """
    Combines exact/alias matching with semantic matching.

    Priority:
        1. Exact skill match
        2. Semantic relationship
        3. Missing skill
    """

    def __init__(
        self,
        semantic_threshold: float = 0.65,
        related_threshold: float = 0.45,
    ):
        if not 0 <= related_threshold <= 1:
            raise ValueError(
                "related_threshold must be between 0 and 1."
            )

        if not 0 <= semantic_threshold <= 1:
            raise ValueError(
                "semantic_threshold must be between 0 and 1."
            )

        if related_threshold > semantic_threshold:
            raise ValueError(
                "related_threshold cannot be greater "
                "than semantic_threshold."
            )

        self.semantic_threshold = semantic_threshold
        self.related_threshold = related_threshold

        self.semantic_matcher = SemanticMatcher()

    # ========================================================
    # EXACT MATCH LOOKUP
    # ========================================================

    @staticmethod
    def build_resume_skill_map(
        resume_skills: list[dict],
    ) -> dict[str, dict]:

        skill_map = {}

        for item in resume_skills:

            skill_name = item.get(
                "skill",
                "",
            )

            normalized = normalize_skill_name(
                skill_name
            )

            if normalized:
                skill_map[normalized] = item

        return skill_map

    # ========================================================
    # HYBRID MATCHING
    # ========================================================

    def match(
        self,
        resume_skills: list[dict],
        jd_skills: list[dict],
    ) -> dict[str, Any]:

        if not isinstance(
            resume_skills,
            list,
        ):
            raise HybridMatcherError(
                "resume_skills must be a list."
            )

        if not isinstance(
            jd_skills,
            list,
        ):
            raise HybridMatcherError(
                "jd_skills must be a list."
            )

        resume_skill_map = (
            self.build_resume_skill_map(
                resume_skills
            )
        )

        results = []

        matched = []
        related = []
        missing = []

        # ----------------------------------------------------
        # Process every JD requirement
        # ----------------------------------------------------

        for jd_skill in jd_skills:

            jd_name = jd_skill.get(
                "skill",
                "",
            )

            if not jd_name:
                continue

            normalized_jd = normalize_skill_name(
                jd_name
            )

            importance = jd_skill.get(
                "importance",
                "general",
            )

            category = jd_skill.get(
                "category",
                "Unknown",
            )

            # ------------------------------------------------
            # 1. EXACT MATCH
            # ------------------------------------------------

            exact_resume_skill = (
                resume_skill_map.get(
                    normalized_jd
                )
            )

            if exact_resume_skill:

                result = {
                    "jd_skill": jd_name,
                    "category": category,
                    "importance": importance,
                    "status": "matched",
                    "match_type": "exact",
                    "similarity": 1.0,
                    "resume_skill": (
                        exact_resume_skill[
                            "skill"
                        ]
                    ),
                    "resume_source": (
                        exact_resume_skill.get(
                            "source"
                        )
                    ),
                    "resume_evidence": (
                        exact_resume_skill.get(
                            "evidence"
                        )
                    ),
                }

                results.append(result)
                matched.append(result)

                continue

            # ------------------------------------------------
            # 2. SEMANTIC MATCH
            # ------------------------------------------------

            best_similarity = 0.0
            best_resume_skill = None

            for resume_skill in resume_skills:

                resume_name = resume_skill.get(
                    "skill",
                    "",
                )

                if not resume_name:
                    continue

                similarity = (
                    self.semantic_matcher
                    .calculate_similarity(
                        jd_name,
                        resume_name,
                    )
                )

                if similarity > best_similarity:

                    best_similarity = similarity
                    best_resume_skill = (
                        resume_skill
                    )

            # ------------------------------------------------
            # 3. SEMANTICALLY MATCHED
            # ------------------------------------------------

            if (
                best_similarity
                >= self.semantic_threshold
            ):

                result = {
                    "jd_skill": jd_name,
                    "category": category,
                    "importance": importance,
                    "status": "matched",
                    "match_type": "semantic",
                    "similarity": best_similarity,
                    "resume_skill": (
                        best_resume_skill[
                            "skill"
                        ]
                        if best_resume_skill
                        else None
                    ),
                    "resume_source": (
                        best_resume_skill.get(
                            "source"
                        )
                        if best_resume_skill
                        else None
                    ),
                    "resume_evidence": (
                        best_resume_skill.get(
                            "evidence"
                        )
                        if best_resume_skill
                        else None
                    ),
                }

                results.append(result)
                matched.append(result)

            # ------------------------------------------------
            # 4. RELATED
            # ------------------------------------------------

            elif (
                best_similarity
                >= self.related_threshold
            ):

                result = {
                    "jd_skill": jd_name,
                    "category": category,
                    "importance": importance,
                    "status": "related",
                    "match_type": "semantic",
                    "similarity": best_similarity,
                    "resume_skill": (
                        best_resume_skill[
                            "skill"
                        ]
                        if best_resume_skill
                        else None
                    ),
                    "resume_source": (
                        best_resume_skill.get(
                            "source"
                        )
                        if best_resume_skill
                        else None
                    ),
                    "resume_evidence": (
                        best_resume_skill.get(
                            "evidence"
                        )
                        if best_resume_skill
                        else None
                    ),
                }

                results.append(result)
                related.append(result)

            # ------------------------------------------------
            # 5. MISSING
            # ------------------------------------------------

            else:

                result = {
                    "jd_skill": jd_name,
                    "category": category,
                    "importance": importance,
                    "status": "missing",
                    "match_type": "none",
                    "similarity": best_similarity,
                    "resume_skill": None,
                    "resume_source": None,
                    "resume_evidence": None,
                }

                results.append(result)
                missing.append(result)

        # ====================================================
        # STATISTICS
        # ====================================================

        required_items = [
            item
            for item in results
            if item["importance"] == "required"
        ]

        preferred_items = [
            item
            for item in results
            if item["importance"] == "preferred"
        ]

        required_matched = [
            item
            for item in required_items
            if item["status"] == "matched"
        ]

        preferred_matched = [
            item
            for item in preferred_items
            if item["status"] == "matched"
        ]

        required_match_percentage = (
            len(required_matched)
            / len(required_items)
            * 100
            if required_items
            else 100.0
        )

        preferred_match_percentage = (
            len(preferred_matched)
            / len(preferred_items)
            * 100
            if preferred_items
            else 100.0
        )

        return {
            "results": results,
            "matched": matched,
            "related": related,
            "missing": missing,
            "statistics": {
                "total": len(results),
                "matched": len(matched),
                "related": len(related),
                "missing": len(missing),
                "required_total": len(
                    required_items
                ),
                "required_matched": len(
                    required_matched
                ),
                "required_match_percentage": round(
                    required_match_percentage,
                    2,
                ),
                "preferred_total": len(
                    preferred_items
                ),
                "preferred_matched": len(
                    preferred_matched
                ),
                "preferred_match_percentage": round(
                    preferred_match_percentage,
                    2,
                ),
            },
        }