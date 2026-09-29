from typing import Any


# ============================================================
# ATS SCORING WEIGHTS
# ============================================================

# These are our project-level engineering weights.
# They are NOT official industry-standard ATS weights.

ATS_WEIGHTS = {
    "required_skills": 50,
    "preferred_skills": 15,
    "semantic_relevance": 10,
    "resume_structure": 15,
    "content_completeness": 10,
}


# ============================================================
# UTILITY
# ============================================================

def clamp_score(score: float) -> float:
    """Keep a score between 0 and 100."""

    return max(
        0.0,
        min(100.0, float(score))
    )


# ============================================================
# MATCH STATUS HELPER
# ============================================================

def is_matched(match_type: str | None) -> bool:
    """
    Decide whether a JD skill has been matched.

    Exact      -> full match
    Semantic   -> semantic match
    Related    -> partial/related match

    Missing    -> not matched
    """

    return match_type in {
        "exact",
        "semantic",
        "related",
    }


# ============================================================
# 1. REQUIRED SKILLS SCORE
# ============================================================

def calculate_required_skill_score(
    hybrid_result: dict[str, Any],
) -> float:
    """
    Calculate required skill coverage directly
    from the hybrid matching results.

    Example:

    Required skills = 11
    Matched skills  = 9

    Score = 81.82
    """

    results = hybrid_result.get("results", [])

    required_results = [
        item
        for item in results
        if item.get("importance") == "required"
    ]

    total = len(required_results)

    if total == 0:
        return 100.0

    matched = sum(
        1
        for item in required_results
        if is_matched(item.get("match_type"))
    )

    score = (
        matched / total
    ) * 100

    return clamp_score(score)


# ============================================================
# 2. PREFERRED SKILLS SCORE
# ============================================================

def calculate_preferred_skill_score(
    hybrid_result: dict[str, Any],
) -> float:
    """
    Calculate preferred skill coverage directly
    from the hybrid matching results.

    Example:

    Preferred skills = 5
    Matched skills   = 3

    Score = 60
    """

    results = hybrid_result.get("results", [])

    preferred_results = [
        item
        for item in results
        if item.get("importance") == "preferred"
    ]

    total = len(preferred_results)

    if total == 0:
        return 100.0

    matched = sum(
        1
        for item in preferred_results
        if is_matched(item.get("match_type"))
    )

    score = (
        matched / total
    ) * 100

    return clamp_score(score)


# ============================================================
# 3. SEMANTIC RELEVANCE SCORE
# ============================================================

def calculate_semantic_relevance_score(
    hybrid_result: dict[str, Any],
) -> float:
    """
    Calculate semantic relevance using
    semantic and related matches only.

    Exact matches are excluded because they are
    already counted in required/preferred coverage.
    """

    results = hybrid_result.get(
        "results",
        []
    )

    semantic_scores = []

    for item in results:

        match_type = item.get(
            "match_type"
        )

        similarity = float(
            item.get(
                "similarity",
                0.0
            )
        )

        # ----------------------------------------------------
        # Exact match
        # ----------------------------------------------------

        if match_type == "exact":
            continue

        # ----------------------------------------------------
        # Semantic match
        # ----------------------------------------------------

        if match_type == "semantic":

            semantic_scores.append(
                similarity
            )

        # ----------------------------------------------------
        # Related match
        # ----------------------------------------------------

        elif match_type == "related":

            semantic_scores.append(
                similarity * 0.5
            )

    if not semantic_scores:
        return 0.0

    average_similarity = (
        sum(semantic_scores)
        / len(semantic_scores)
    )

    return clamp_score(
        average_similarity * 100
    )


# ============================================================
# 4. RESUME STRUCTURE SCORE
# ============================================================

def calculate_resume_structure_score(
    resume_analysis: dict[str, Any],
) -> float:
    """
    Check whether the resume contains
    important structural sections.

    Expected:

    - Skills
    - Education
    - Experience
    - Projects
    """

    nlp_data = resume_analysis.get(
        "nlp",
        {}
    )

    sections = nlp_data.get(
        "sections",
        {}
    )

    expected_sections = [
        "skills",
        "education",
        "experience",
        "projects",
    ]

    found_sections = 0

    for section in expected_sections:

        section_data = sections.get(
            section
        )

        if section_data:
            found_sections += 1

    score = (
        found_sections
        / len(expected_sections)
    ) * 100

    return clamp_score(score)


# ============================================================
# 5. CONTENT COMPLETENESS SCORE
# ============================================================

def calculate_content_completeness_score(
    resume_analysis: dict[str, Any],
) -> float:
    """
    Check whether the resume contains
    enough meaningful content.

    Four checks:

    1. Text length
    2. Token count
    3. Sentence count
    4. Number of detected skills

    Each contributes 25%.
    """

    raw_text = resume_analysis.get(
        "raw_text",
        ""
    )

    nlp_data = resume_analysis.get(
        "nlp",
        {}
    )

    token_count = nlp_data.get(
        "token_count",
        0
    )

    sentence_count = nlp_data.get(
        "sentence_count",
        0
    )

    skills = resume_analysis.get(
        "skills",
        []
    )

    score = 0.0

    # --------------------------------------------------------
    # Check 1: meaningful text
    # --------------------------------------------------------

    if len(raw_text.strip()) >= 500:
        score += 25

    # --------------------------------------------------------
    # Check 2: token count
    # --------------------------------------------------------

    if token_count >= 100:
        score += 25

    # --------------------------------------------------------
    # Check 3: sentence count
    # --------------------------------------------------------

    if sentence_count >= 5:
        score += 25

    # --------------------------------------------------------
    # Check 4: skills
    # --------------------------------------------------------

    if len(skills) >= 3:
        score += 25

    return clamp_score(score)


# ============================================================
# MAIN ATS SCORE
# ============================================================

def calculate_ats_score(
    resume_analysis: dict[str, Any],
    hybrid_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate final ATS score.

    Pipeline:

        Required Skills
              +
        Preferred Skills
              +
        Semantic Relevance
              +
        Resume Structure
              +
        Content Completeness
              ↓
        Final ATS Score
    """

    # ========================================================
    # COMPONENT 1
    # ========================================================

    required_score = (
        calculate_required_skill_score(
            hybrid_result
        )
    )

    # ========================================================
    # COMPONENT 2
    # ========================================================

    preferred_score = (
        calculate_preferred_skill_score(
            hybrid_result
        )
    )

    # ========================================================
    # COMPONENT 3
    # ========================================================

    semantic_score = (
        calculate_semantic_relevance_score(
            hybrid_result
        )
    )

    # ========================================================
    # COMPONENT 4
    # ========================================================

    structure_score = (
        calculate_resume_structure_score(
            resume_analysis
        )
    )

    # ========================================================
    # COMPONENT 5
    # ========================================================

    completeness_score = (
        calculate_content_completeness_score(
            resume_analysis
        )
    )

    # ========================================================
    # COMPONENT SCORES
    # ========================================================

    components = {

        "required_skills": round(
            required_score,
            2,
        ),

        "preferred_skills": round(
            preferred_score,
            2,
        ),

        "semantic_relevance": round(
            semantic_score,
            2,
        ),

        "resume_structure": round(
            structure_score,
            2,
        ),

        "content_completeness": round(
            completeness_score,
            2,
        ),
    }

    # ========================================================
    # WEIGHTED CONTRIBUTION
    # ========================================================

    weighted_contribution = {}

    for component_name, weight in ATS_WEIGHTS.items():

        contribution = (
            components[component_name]
            * weight
            / 100
        )

        weighted_contribution[
            component_name
        ] = round(
            contribution,
            2,
        )

    # ========================================================
    # FINAL SCORE
    # ========================================================

    final_score = sum(
        weighted_contribution.values()
    )

    final_score = clamp_score(
        final_score
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "ats_score": round(
            final_score,
            2,
        ),

        "components": components,

        "weights": ATS_WEIGHTS,

        "weighted_contribution":
            weighted_contribution,
    }