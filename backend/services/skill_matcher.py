from typing import Any


class SkillMatcherError(Exception):
    """Base exception for skill matching errors."""


def normalize_skill_name(skill: str) -> str:
    """
    Normalize skill names before comparison.

    This makes comparisons case-insensitive and removes
    small formatting differences.
    """

    if not skill:
        return ""

    return (
        skill.lower()
        .strip()
        .replace("-", "")
        .replace(" ", "")
        .replace(".", "")
        .replace("_", "")
    )


def build_resume_skill_map(
    resume_skills: list[dict],
) -> dict[str, dict]:
    """
    Create a normalized lookup map from extracted resume skills.
    """

    skill_map = {}

    for item in resume_skills:

        skill_name = item.get("skill", "")

        normalized = normalize_skill_name(
            skill_name
        )

        if not normalized:
            continue

        skill_map[normalized] = item

    return skill_map


def match_jd_skills(
    resume_skills: list[dict],
    jd_skills: list[dict],
) -> dict[str, Any]:
    """
    Compare resume skills against Job Description skills.
    """

    if not isinstance(resume_skills, list):
        raise SkillMatcherError(
            "resume_skills must be a list."
        )

    if not isinstance(jd_skills, list):
        raise SkillMatcherError(
            "jd_skills must be a list."
        )

    resume_skill_map = build_resume_skill_map(
        resume_skills
    )

    matched_required = []
    missing_required = []

    matched_preferred = []
    missing_preferred = []

    matched_general = []
    missing_general = []

    for jd_skill in jd_skills:

        skill_name = jd_skill.get(
            "skill",
            "",
        )

        normalized_skill = normalize_skill_name(
            skill_name
        )

        importance = jd_skill.get(
            "importance",
            "general",
        )

        if not normalized_skill:
            continue

        resume_skill = resume_skill_map.get(
            normalized_skill
        )

        match_data = {
            "skill": skill_name,
            "category": jd_skill.get(
                "category",
                "Unknown",
            ),
            "importance": importance,
            "resume_evidence": (
                resume_skill.get(
                    "evidence",
                    "",
                )
                if resume_skill
                else None
            ),
            "resume_source": (
                resume_skill.get(
                    "source",
                    "",
                )
                if resume_skill
                else None
            ),
        }

        if resume_skill:

            if importance == "required":
                matched_required.append(
                    match_data
                )

            elif importance == "preferred":
                matched_preferred.append(
                    match_data
                )

            else:
                matched_general.append(
                    match_data
                )

        else:

            if importance == "required":
                missing_required.append(
                    match_data
                )

            elif importance == "preferred":
                missing_preferred.append(
                    match_data
                )

            else:
                missing_general.append(
                    match_data
                )

    # --------------------------------------------------------
    # MATCH PERCENTAGES
    # --------------------------------------------------------

    required_total = (
        len(matched_required)
        + len(missing_required)
    )

    preferred_total = (
        len(matched_preferred)
        + len(missing_preferred)
    )

    general_total = (
        len(matched_general)
        + len(missing_general)
    )

    required_match_percentage = (
        len(matched_required)
        / required_total
        * 100
        if required_total
        else 100.0
    )

    preferred_match_percentage = (
        len(matched_preferred)
        / preferred_total
        * 100
        if preferred_total
        else 100.0
    )

    overall_total = (
        required_total
        + preferred_total
        + general_total
    )

    overall_matched = (
        len(matched_required)
        + len(matched_preferred)
        + len(matched_general)
    )

    overall_match_percentage = (
        overall_matched
        / overall_total
        * 100
        if overall_total
        else 0.0
    )

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "matched_general": matched_general,
        "missing_general": missing_general,
        "required_match_percentage": round(
            required_match_percentage,
            2,
        ),
        "preferred_match_percentage": round(
            preferred_match_percentage,
            2,
        ),
        "overall_match_percentage": round(
            overall_match_percentage,
            2,
        ),
        "statistics": {
            "required_total": required_total,
            "required_matched": len(
                matched_required
            ),
            "required_missing": len(
                missing_required
            ),
            "preferred_total": preferred_total,
            "preferred_matched": len(
                matched_preferred
            ),
            "preferred_missing": len(
                missing_preferred
            ),
            "overall_total": overall_total,
            "overall_matched": overall_matched,
        },
    }