from typing import Any


# ============================================================
# FEEDBACK ENGINE
# ============================================================

class FeedbackEngine:
    """
    Generates explainable feedback from:

    1. Resume analysis
    2. Hybrid JD matching
    3. ATS scoring

    No LLM is used here.

    This makes the feedback:
    - deterministic
    - explainable
    - reproducible
    - easy to debug
    """

    def __init__(
        self,
        resume_analysis: dict[str, Any],
        hybrid_result: dict[str, Any],
        ats_result: dict[str, Any],
    ):
        self.resume_analysis = resume_analysis
        self.hybrid_result = hybrid_result
        self.ats_result = ats_result

    # ========================================================
    # 1. STRENGTHS
    # ========================================================

    def generate_strengths(self) -> list[str]:
        """
        Identify strong areas of the resume.
        """

        strengths = []

        components = self.ats_result.get(
            "components",
            {}
        )

        required_score = components.get(
            "required_skills",
            0
        )

        preferred_score = components.get(
            "preferred_skills",
            0
        )

        structure_score = components.get(
            "resume_structure",
            0
        )

        completeness_score = components.get(
            "content_completeness",
            0
        )

        # ----------------------------------------------------
        # Required skills
        # ----------------------------------------------------

        if required_score >= 90:

            strengths.append(
                "Strong coverage of the required job skills."
            )

        elif required_score >= 70:

            strengths.append(
                "Good coverage of the required job skills."
            )

        # ----------------------------------------------------
        # Preferred skills
        # ----------------------------------------------------

        if preferred_score >= 90:

            strengths.append(
                "Strong coverage of the preferred job skills."
            )

        elif preferred_score >= 70:

            strengths.append(
                "Good coverage of the preferred job skills."
            )

        # ----------------------------------------------------
        # Resume structure
        # ----------------------------------------------------

        if structure_score >= 90:

            strengths.append(
                "Resume contains the important sections "
                "needed for structured analysis."
            )

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------

        if completeness_score >= 90:

            strengths.append(
                "Resume contains sufficient textual and "
                "technical content."
            )

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        if not strengths:

            strengths.append(
                "Resume has a foundation that can be "
                "improved through targeted changes."
            )

        return strengths

    # ========================================================
    # 2. MISSING SKILLS
    # ========================================================

    def get_missing_skills(self) -> list[dict[str, Any]]:
        """
        Return skills from the JD that were not matched.

        HybridMatcher stores JD importance as:
            required
            preferred
            general

        Feedback Engine exposes the same value as priority
        because the feedback/recommendation layer uses the
        term "priority".
        """

        results = self.hybrid_result.get(
            "results",
            []
        )

        missing_skills = []

        for item in results:

            if item.get("status") == "missing":

                importance = item.get(
                    "importance",
                    "general",
                )

                missing_skills.append(
                    {
                        "skill": item.get(
                            "jd_skill"
                        ),

                        "category": item.get(
                            "category"
                        ),

                        "priority": importance,
                    }
                )

        return missing_skills

    # ========================================================
    # 3. RELATED SKILLS
    # ========================================================

    def get_related_skills(self) -> list[dict[str, Any]]:
        """
        Return skills that were considered related
        through semantic matching.
        """

        results = self.hybrid_result.get(
            "results",
            []
        )

        related_skills = []

        for item in results:

            if item.get("status") == "related":

                related_skills.append(
                    {
                        "jd_skill": item.get(
                            "jd_skill"
                        ),
                        "resume_skill": item.get(
                            "resume_skill"
                        ),
                        "similarity": round(
                            float(
                                item.get(
                                    "similarity",
                                    0.0
                                )
                            ),
                            3,
                        ),
                    }
                )

        return related_skills

    # ========================================================
    # 4. IMPROVEMENTS
    # ========================================================

    def generate_improvements(self) -> list[str]:
        """
        Generate actionable resume improvements.
        """

        improvements = []

        components = self.ats_result.get(
            "components",
            {}
        )

        required_score = components.get(
            "required_skills",
            0
        )

        preferred_score = components.get(
            "preferred_skills",
            0
        )

        structure_score = components.get(
            "resume_structure",
            0
        )

        completeness_score = components.get(
            "content_completeness",
            0
        )

        missing_skills = self.get_missing_skills()

        related_skills = self.get_related_skills()

        # ----------------------------------------------------
        # Missing required skills
        # ----------------------------------------------------

        required_missing = [
            item
            for item in missing_skills
            if item.get("priority") == "required"
        ]

        if required_missing:

            skill_names = [
                item["skill"]
                for item in required_missing
            ]

            improvements.append(
                "Review the missing required skills: "
                + ", ".join(skill_names)
                + ". Add them only if you genuinely "
                  "have experience with them."
            )

        # ----------------------------------------------------
        # Missing preferred skills
        # ----------------------------------------------------

        preferred_missing = [
            item
            for item in missing_skills
            if item.get("priority") == "preferred"
        ]

        if preferred_missing:

            skill_names = [
                item["skill"]
                for item in preferred_missing
            ]

            improvements.append(
                "Consider adding relevant preferred skills "
                "if you have genuine experience with: "
                + ", ".join(skill_names)
                + "."
            )

        # ----------------------------------------------------
        # Required skill coverage
        # ----------------------------------------------------

        if required_score < 70:

            improvements.append(
                "Improve alignment with the job description "
                "by demonstrating more of the required skills "
                "through projects or experience."
            )

        # ----------------------------------------------------
        # Preferred skill coverage
        # ----------------------------------------------------

        elif preferred_score < 70:

            improvements.append(
                "Improve coverage of preferred skills where "
                "you have relevant experience."
            )

        # ----------------------------------------------------
        # Resume structure
        # ----------------------------------------------------

        if structure_score < 75:

            improvements.append(
                "Improve resume structure by clearly "
                "organizing sections such as Skills, "
                "Education, Experience and Projects."
            )

        # ----------------------------------------------------
        # Content completeness
        # ----------------------------------------------------

        if completeness_score < 75:

            improvements.append(
                "Add more meaningful technical and project "
                "details to make the resume more informative."
            )

        # ----------------------------------------------------
        # Related skills
        # ----------------------------------------------------

        if related_skills:

            improvements.append(
                "Review semantically related skills and "
                "make the connection explicit in project "
                "or experience descriptions where accurate."
            )

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        if not improvements:

            improvements.append(
                "No major improvements were identified "
                "from the current automated analysis."
            )

        return improvements

    # ========================================================
    # 5. SUMMARY
    # ========================================================

    def generate_summary(self) -> str:
        """
        Generate a concise textual summary.
        """

        score = self.ats_result.get(
            "ats_score",
            0
        )

        missing_count = len(
            self.get_missing_skills()
        )

        if score >= 85:

            level = "strong"

        elif score >= 70:

            level = "moderate"

        else:

            level = "needs improvement"

        if missing_count == 0:

            missing_text = (
                "No unmatched JD skills were detected."
            )

        else:

            missing_text = (
                f"{missing_count} JD skill(s) "
                "were not matched."
            )

        return (
            f"The resume shows a {level} alignment "
            f"with the analyzed job description. "
            f"{missing_text}"
        )

    # ========================================================
    # 6. COMPLETE FEEDBACK
    # ========================================================

    def generate_feedback(self) -> dict[str, Any]:
        """
        Generate the complete feedback response.
        """

        return {
            "summary": self.generate_summary(),

            "strengths": self.generate_strengths(),

            "missing_skills": self.get_missing_skills(),

            "related_skills": self.get_related_skills(),

            "improvements": self.generate_improvements(),
        }


# ============================================================
# CONVENIENCE FUNCTION
# ============================================================

def generate_feedback(
    resume_analysis: dict[str, Any],
    hybrid_result: dict[str, Any],
    ats_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Simple function-based interface.
    """

    engine = FeedbackEngine(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
        ats_result=ats_result,
    )

    return engine.generate_feedback()