from typing import Any


class RecommendationEngine:
    """
    Converts ATS feedback into actionable recommendations.

    Input:
        - resume analysis
        - hybrid matching result
        - ATS score
        - feedback

    Output:
        - skill recommendations
        - semantic alignment recommendations
        - resume structure recommendations
        - content recommendations
        - ATS recommendations
    """

    def __init__(
        self,
        resume_analysis: dict[str, Any],
        hybrid_result: dict[str, Any],
        ats_result: dict[str, Any],
        feedback: dict[str, Any],
    ):
        self.resume_analysis = resume_analysis
        self.hybrid_result = hybrid_result
        self.ats_result = ats_result
        self.feedback = feedback

    # ========================================================
    # 1. SKILL RECOMMENDATIONS
    # ========================================================

    def generate_skill_recommendations(self) -> list[dict[str, Any]]:
        """
        Generate recommendations for missing JD skills.

        Important:
        We never tell the user to falsely add a skill.
        """

        recommendations = []

        missing_skills = self.feedback.get(
            "missing_skills",
            [],
        )

        for item in missing_skills:

            skill = item.get(
                "skill",
                "Unknown skill",
            )

            priority = item.get(
                "priority",
                "general",
            )

            if priority == "required":
                importance = "high"

            elif priority == "preferred":
                importance = "medium"

            else:
                importance = "low"

            recommendations.append(
                {
                    "type": "skill",
                    "title": skill,
                    "skill": skill,
                    "priority": importance,
                    "recommendation": (
                        f"If you genuinely have experience "
                        f"with {skill}, make that experience "
                        f"explicit in your resume."
                    ),
                    "suggested_action": (
                        f"Add {skill} to the Skills section "
                        f"and mention where you actually used "
                        f"it in a project or experience entry."
                    ),
                }
            )

        return recommendations

    # ========================================================
    # 2. RELATED SKILL RECOMMENDATIONS
    # ========================================================

    def generate_related_skill_recommendations(
        self,
    ) -> list[dict[str, Any]]:
        """
        Explain how semantically related skills
        could be made clearer.
        """

        recommendations = []

        related_skills = self.feedback.get(
            "related_skills",
            [],
        )

        for item in related_skills:

            jd_skill = item.get(
                "jd_skill",
                "Unknown",
            )

            resume_skill = item.get(
                "resume_skill",
                "Unknown",
            )

            recommendations.append(
                {
                    "type": "semantic_alignment",
                    "title": f"Clarify {jd_skill}",
                    "priority": "medium",
                    "jd_skill": jd_skill,
                    "resume_skill": resume_skill,
                    "recommendation": (
                        f"The resume contains "
                        f"'{resume_skill}', which is "
                        f"semantically related to "
                        f"'{jd_skill}'."
                    ),
                    "suggested_action": (
                        f"If accurate, explicitly mention "
                        f"'{jd_skill}' in the relevant project "
                        f"or experience description."
                    ),
                }
            )

        return recommendations

    # ========================================================
    # 3. STRUCTURE RECOMMENDATIONS
    # ========================================================

    def generate_structure_recommendations(
        self,
    ) -> list[dict[str, Any]]:
        """
        Recommend structural improvements.
        """

        recommendations = []

        components = self.ats_result.get(
            "components",
            {},
        )

        structure_score = components.get(
            "resume_structure",
            0,
        )

        nlp_data = self.resume_analysis.get(
            "nlp",
            {},
        )

        sections = nlp_data.get(
            "sections",
            {},
        )

        if structure_score < 75:

            missing_sections = []

            for section in [
                "skills",
                "education",
                "experience",
                "projects",
            ]:

                if not sections.get(section):
                    missing_sections.append(
                        section.title()
                    )

            recommendations.append(
                {
                    "type": "structure",
                    "title": "Improve Resume Structure",
                    "priority": "high",
                    "missing_sections": missing_sections,
                    "recommendation": (
                        "Improve the organization of "
                        "the resume."
                    ),
                    "suggested_action": (
                        "Add or clearly label the important "
                        "resume sections."
                    ),
                }
            )

        return recommendations

    # ========================================================
    # 4. CONTENT RECOMMENDATIONS
    # ========================================================

    def generate_content_recommendations(
        self,
    ) -> list[dict[str, Any]]:
        """
        Recommend improvements to resume content.
        """

        recommendations = []

        components = self.ats_result.get(
            "components",
            {},
        )

        content_score = components.get(
            "content_completeness",
            0,
        )

        if content_score < 75:

            recommendations.append(
                {
                    "type": "content",
                    "title": "Improve Resume Content",
                    "priority": "medium",
                    "recommendation": (
                        "The resume may need more "
                        "meaningful content."
                    ),
                    "suggested_action": (
                        "Add concise project descriptions, "
                        "technical details, responsibilities, "
                        "and measurable outcomes where "
                        "applicable."
                    ),
                }
            )

        return recommendations

    # ========================================================
    # 5. ATS RECOMMENDATIONS
    # ========================================================

    def generate_ats_recommendations(
        self,
    ) -> list[dict[str, Any]]:
        """
        Generate ATS recommendations only when there is
        a meaningful score-related issue.

        Each recommendation has a proper title so the
        frontend does not display "Recommendation 1",
        "Recommendation 2", etc.
        """

        recommendations = []

        ats_score = self.ats_result.get(
            "ats_score",
            0,
        )

        components = self.ats_result.get(
            "components",
            {},
        )

        required_score = components.get(
            "required_skills",
            0,
        )

        preferred_score = components.get(
            "preferred_skills",
            0,
        )

        structure_score = components.get(
            "resume_structure",
            0,
        )

        content_score = components.get(
            "content_completeness",
            0,
        )

        # --------------------------------------------------------
        # 1. Required skills
        # --------------------------------------------------------

        if required_score < 75:

            recommendations.append(
                {
                    "type": "ats",
                    "title": "Improve Required Skill Coverage",
                    "priority": "high",
                    "recommendation": (
                        f"Required skill coverage is "
                        f"{required_score:.0f}%. Focus on the "
                        f"missing required skills identified above."
                    ),
                    "suggested_action": (
                        "Review the missing required skills and "
                        "make relevant experience explicit where "
                        "you genuinely have it."
                    ),
                }
            )

        # --------------------------------------------------------
        # 2. Preferred skills
        # --------------------------------------------------------

        elif preferred_score < 75:

            recommendations.append(
                {
                    "type": "ats",
                    "title": "Improve Preferred Skill Coverage",
                    "priority": "medium",
                    "recommendation": (
                        f"Preferred skill coverage is "
                        f"{preferred_score:.0f}%. Some optional "
                        f"job-specific skills are missing."
                    ),
                    "suggested_action": (
                        "If you have genuine experience with "
                        "the missing preferred skills, highlight "
                        "that experience in relevant projects "
                        "or work."
                    ),
                }
            )

        # --------------------------------------------------------
        # 3. Resume structure
        # --------------------------------------------------------

        if structure_score < 75:

            recommendations.append(
                {
                    "type": "ats",
                    "title": "Improve Resume Structure",
                    "priority": "high",
                    "recommendation": (
                        f"Resume structure scored "
                        f"{structure_score:.0f}%. Important "
                        f"sections may not be clearly identified."
                    ),
                    "suggested_action": (
                        "Use clear sections such as Skills, "
                        "Education, Experience and Projects."
                    ),
                }
            )

        # --------------------------------------------------------
        # 4. Content completeness
        # --------------------------------------------------------

        if content_score < 75:

            recommendations.append(
                {
                    "type": "ats",
                    "title": "Improve Resume Content",
                    "priority": "medium",
                    "recommendation": (
                        f"Content completeness scored "
                        f"{content_score:.0f}%. The resume may "
                        f"need more relevant technical or "
                        f"project detail."
                    ),
                    "suggested_action": (
                        "Add concise technical details, project "
                        "responsibilities and measurable outcomes "
                        "where applicable."
                    ),
                }
            )

        # --------------------------------------------------------
        # 5. Very low overall ATS score
        # --------------------------------------------------------

        if ats_score < 60 and not recommendations:

            recommendations.append(
                {
                    "type": "ats",
                    "title": "Improve Overall ATS Alignment",
                    "priority": "high",
                    "recommendation": (
                        f"The overall ATS score is "
                        f"{ats_score:.0f}%. Several areas of "
                        f"the resume may need improvement."
                    ),
                    "suggested_action": (
                        "Review required skills, resume "
                        "structure and content completeness."
                    ),
                }
            )

        return recommendations

    # ========================================================
    # 6. ALL RECOMMENDATIONS
    # ========================================================

    def generate_recommendations(
        self,
    ) -> dict[str, Any]:
        """
        Generate the complete recommendation response.
        """

        skill_recommendations = (
            self.generate_skill_recommendations()
        )

        related_recommendations = (
            self.generate_related_skill_recommendations()
        )

        structure_recommendations = (
            self.generate_structure_recommendations()
        )

        content_recommendations = (
            self.generate_content_recommendations()
        )

        ats_recommendations = (
            self.generate_ats_recommendations()
        )

        all_recommendations = (
            skill_recommendations
            + related_recommendations
            + structure_recommendations
            + content_recommendations
            + ats_recommendations
        )

        return {
            "skill_recommendations": (
                skill_recommendations
            ),

            "related_skill_recommendations": (
                related_recommendations
            ),

            "structure_recommendations": (
                structure_recommendations
            ),

            "content_recommendations": (
                content_recommendations
            ),

            "ats_recommendations": (
                ats_recommendations
            ),

            "recommendations": (
                all_recommendations
            ),

            "total": len(
                all_recommendations
            ),
        }


# ============================================================
# CONVENIENCE FUNCTION
# ============================================================

def generate_recommendations(
    resume_analysis: dict[str, Any],
    hybrid_result: dict[str, Any],
    ats_result: dict[str, Any],
    feedback: dict[str, Any],
) -> dict[str, Any]:

    engine = RecommendationEngine(
        resume_analysis=resume_analysis,
        hybrid_result=hybrid_result,
        ats_result=ats_result,
        feedback=feedback,
    )

    return engine.generate_recommendations()