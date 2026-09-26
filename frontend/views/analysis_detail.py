import os
import tempfile
import streamlit as st

from backend.services.report_generator import generate_ats_report


def render_analysis_detail():
    """
    Render a complete saved resume analysis.
    """

    # =========================================================
    # GET SELECTED ANALYSIS
    # =========================================================

    analysis = st.session_state.get(
        "selected_history_analysis"
    )

    if not analysis:

        st.warning("No analysis selected.")

        if st.button("← Back to History"):

            st.session_state["current_page"] = "history"
            st.rerun()

        return

    # =========================================================
    # EXTRACT DATA
    # =========================================================

    filename = analysis.get(
        "filename",
        "Resume",
    )

    ats_score = float(
        analysis.get(
            "ats_score",
            0,
        )
    )

    keyword_match = float(
        analysis.get(
            "keyword_match",
            0,
        )
    )

    missing_keywords = analysis.get(
        "missing_keywords",
        [],
    )

    result = analysis.get(
        "analysis_result",
        {},
    )

    ats_data = result.get(
        "ats",
        {},
    )

    components = ats_data.get(
        "components",
        {},
    )

    matching_data = result.get(
        "matching",
        {},
    )

    feedback_data = result.get(
        "feedback",
        {},
    )

    recommendation_data = result.get(
        "recommendations",
        {},
    )

    # =========================================================
    # PAGE HEADER
    # =========================================================

    if st.button(
        "← Back to History",
        type="secondary",
    ):

        st.session_state["current_page"] = "history"
        st.rerun()

    st.markdown("")

    st.title("📄 Analysis Details")

    st.caption(
        f"Saved analysis for **{filename}**"
    )

    st.divider()

    # =========================================================
    # ATS SCORE
    # =========================================================

    st.markdown("### 🎯 ATS Score")

    score_col1, score_col2 = st.columns(
        [1, 2],
        gap="large",
    )

    # ---------------------------------------------------------
    # MAIN SCORE
    # ---------------------------------------------------------

    with score_col1:

        with st.container(border=True):

            st.caption(
                "OVERALL ATS SCORE"
            )

            # ---------------------------------------------------------
            # ATS SCORE VALUE
            # ---------------------------------------------------------

            st.metric(
                label="ATS Score",
                value=f"{ats_score:.0f}/100",
            )

            st.progress(
                min(
                    max(ats_score / 100, 0.0),
                    1.0,
                ),
                text=f"{ats_score:.0f}% ATS compatibility",
            )

            if ats_score >= 80:

                st.success(
                    "🟢 Strong ATS compatibility"
                )

            elif ats_score >= 60:

                st.warning(
                    "🟡 Moderate ATS compatibility"
                )

            else:

                st.error(
                    "🔴 Resume needs improvement"
                )

    # ---------------------------------------------------------
    # SCORE OVERVIEW
    # ---------------------------------------------------------

    with score_col2:

        with st.container(border=True):

            st.markdown(
                "#### Score Overview"
            )

            st.caption(
                "Your resume's compatibility "
                "with the target job description."
            )

            st.progress(
                min(
                    max(
                        ats_score / 100,
                        0.0,
                    ),
                    1.0,
                ),
                text=(
                    f"{ats_score:.0f}% "
                    "ATS compatibility"
                ),
            )

            st.markdown("")

            info_col1, info_col2 = st.columns(2)

            with info_col1:

                st.metric(
                    "Keyword Match",
                    f"{keyword_match:.0f}%",
                )

            with info_col2:

                st.metric(
                    "Missing Skills",
                    len(missing_keywords),
                )

    # =========================================================
    # ATS SCORE BREAKDOWN
    # =========================================================

    st.markdown("")
    st.markdown("### 📊 ATS Score Breakdown")

    st.caption(
        "See how your resume performed across each ATS dimension."
    )

    breakdown = [
        (
            "🎯",
            "Required Skills",
            components.get(
                "required_skills",
                0,
            ),
            "Core skills requested by the job.",
        ),
        (
            "⭐",
            "Preferred Skills",
            components.get(
                "preferred_skills",
                0,
            ),
            "Additional skills marked as preferred.",
        ),
        (
            "🧠",
            "Semantic Relevance",
            components.get(
                "semantic_relevance",
                0,
            ),
            "Meaning-level similarity with the job.",
        ),
        (
            "📄",
            "Resume Structure",
            components.get(
                "resume_structure",
                0,
            ),
            "Presence of important resume sections.",
        ),
        (
            "📝",
            "Content Completeness",
            components.get(
                "content_completeness",
                0,
            ),
            "Overall resume content coverage.",
        ),
    ]

    for i in range(
        0,
        len(breakdown),
        3,
    ):

        row = breakdown[i:i + 3]

        columns = st.columns(
            len(row),
            gap="medium",
        )

        for column, item in zip(
            columns,
            row,
        ):

            icon, title, score, description = item

            score = float(score)

            with column:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"""
                        <div style="
                            font-size:1.5rem;
                            margin-bottom:8px;
                        ">
                            {icon}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"**{title}**"
                    )

                    st.markdown(
                        f"""
                        <div style="
                            color:#a78bfa;
                            font-size:2rem;
                            font-weight:800;
                            margin:5px 0;
                        ">
                            {score:.0f}%
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.caption(
                        description
                    )

                    st.progress(
                        min(
                            max(
                                score / 100,
                                0.0,
                            ),
                            1.0,
                        )
                    )

    # =========================================================
    # SKILL MATCHING
    # =========================================================

    st.markdown("")
    st.markdown("### 🎯 Skill Matching")

    st.caption(
        "Understand which job skills are present, related, or missing."
    )

    matched_skills = matching_data.get(
        "matched",
        [],
    )

    related_skills = matching_data.get(
        "related",
        [],
    )

    missing_skills = matching_data.get(
        "missing",
        [],
    )

    # =========================================================
    # MATCHED SKILLS
    # =========================================================

    st.markdown("#### 🟢 Matched Skills")

    if matched_skills:

        for i in range(
            0,
            len(matched_skills),
            3,
        ):

            row = matched_skills[i:i + 3]

            columns = st.columns(
                3,
                gap="medium",
            )

            for column, skill in zip(
                columns,
                row,
            ):

                with column:

                    with st.container(
                        border=True
                    ):

                        skill_name = skill.get(
                            "jd_skill",
                            "Unknown",
                        )

                        importance = str(
                            skill.get(
                                "importance",
                                "general",
                            )
                        ).lower()

                        match_type = str(
                            skill.get(
                                "match_type",
                                "exact",
                            )
                        ).lower()

                        st.markdown(
                            f"**{skill_name}**"
                        )

                        if importance == "required":

                            st.success(
                                f"REQUIRED • {match_type.upper()}"
                            )

                        elif importance == "preferred":

                            st.info(
                                f"PREFERRED • {match_type.upper()}"
                            )

                        else:

                            st.caption(
                                f"GENERAL • {match_type.upper()}"
                            )

    else:

        st.info(
            "No matched skills found."
        )

    # =========================================================
    # RELATED SKILLS
    # =========================================================

    if related_skills:

        st.markdown("")
        st.markdown("#### 🟡 Related Skills")

        for i in range(
            0,
            len(related_skills),
            2,
        ):

            row = related_skills[i:i + 2]

            columns = st.columns(
                2,
                gap="medium",
            )

            for column, skill in zip(
                columns,
                row,
            ):

                with column:

                    with st.container(
                        border=True
                    ):

                        jd_skill = skill.get(
                            "jd_skill",
                            "Unknown",
                        )

                        resume_skill = skill.get(
                            "resume_skill",
                            "Unknown",
                        )

                        similarity = float(
                            skill.get(
                                "similarity",
                                0,
                            )
                        )

                        st.markdown(
                            f"**{jd_skill}**"
                        )

                        st.caption(
                            f"Resume skill: {resume_skill}"
                        )

                        st.progress(
                            min(
                                max(
                                    similarity,
                                    0.0,
                                ),
                                1.0,
                            ),
                            text=(
                                f"{similarity * 100:.1f}% "
                                "semantic similarity"
                            ),
                        )

    # =========================================================
    # MISSING SKILLS
    # =========================================================

    st.markdown("")
    st.markdown("#### 🔴 Missing Skills")

    if missing_skills:

        for skill in missing_skills:

            skill_name = skill.get(
                "jd_skill",
                "Unknown",
            )

            importance = str(
                skill.get(
                    "importance",
                    "general",
                )
            ).lower()

            category = skill.get(
                "category",
                "General",
            )

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1],
                    gap="medium",
                )

                with col1:

                    st.markdown(
                        f"**{skill_name}**"
                    )

                    st.caption(
                        category
                    )

                with col2:

                    if importance == "required":

                        st.error(
                            "REQUIRED"
                        )

                    elif importance == "preferred":

                        st.warning(
                            "PREFERRED"
                        )

                    else:

                        st.caption(
                            "GENERAL"
                        )

    else:

        st.success(
            "🎉 No missing skills detected!"
        )

    # =========================================================
    # RESUME FEEDBACK
    # =========================================================

    st.markdown("")
    st.markdown("### 💡 Resume Feedback")

    st.caption(
        "Understand what is working well and what can be improved."
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    summary = feedback_data.get(
        "summary",
        "No summary available.",
    )

    with st.container(
        border=True
    ):

        st.markdown(
            "#### 📋 Overall Summary"
        )

        st.write(summary)

    # ---------------------------------------------------------
    # STRENGTHS
    # ---------------------------------------------------------

    strengths = feedback_data.get(
        "strengths",
        [],
    )

    st.markdown("#### 🟢 Strengths")

    if strengths:

        for strength in strengths:

            if isinstance(
                strength,
                dict,
            ):

                title = strength.get(
                    "title",
                    strength.get(
                        "message",
                        "Strength",
                    ),
                )

                description = strength.get(
                    "description",
                    "",
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**{title}**"
                    )

                    if description:

                        st.write(
                            description
                        )

            else:

                with st.container(
                    border=True
                ):

                    st.write(
                        str(strength)
                    )

    else:

        st.info(
            "No specific strengths identified."
        )

    # ---------------------------------------------------------
    # IMPROVEMENTS
    # ---------------------------------------------------------

    improvements = feedback_data.get(
        "improvements",
        [],
    )

    st.markdown("#### ⚠️ Improvements")

    if improvements:

        for improvement in improvements:

            if isinstance(
                improvement,
                dict,
            ):

                title = improvement.get(
                    "title",
                    improvement.get(
                        "message",
                        "Improvement",
                    ),
                )

                description = improvement.get(
                    "description",
                    "",
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**{title}**"
                    )

                    if description:

                        st.write(
                            description
                        )

            else:

                with st.container(
                    border=True
                ):

                    st.write(
                        str(improvement)
                    )

    else:

        st.info(
            "No specific improvements identified."
        )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    st.markdown("")
    st.markdown("### 🚀 Recommendations")

    st.caption(
        "Actionable suggestions based on this analysis."
    )

    all_recommendations = []

    if isinstance(
        recommendation_data,
        dict,
    ):

        for key, items in recommendation_data.items():

            if isinstance(
                items,
                list,
            ):

                for item in items:

                    all_recommendations.append(
                        (
                            key,
                            item,
                        )
                    )

            elif items:

                all_recommendations.append(
                    (
                        key,
                        items,
                    )
                )

    elif isinstance(
        recommendation_data,
        list,
    ):

        for item in recommendation_data:

            all_recommendations.append(
                (
                    "recommendation",
                    item,
                )
            )

    if all_recommendations:

        for index, (
            rec_type,
            rec_data,
        ) in enumerate(
            all_recommendations,
            start=1,
        ):

            if isinstance(
                rec_data,
                dict,
            ):

                title = rec_data.get(
                    "skill",
                    rec_data.get(
                        "title",
                        f"Recommendation {index}",
                    ),
                )

                message = rec_data.get(
                    "message",
                    rec_data.get(
                        "recommendation",
                        rec_data.get(
                            "description",
                            "",
                        ),
                    ),
                )

                priority = rec_data.get(
                    "priority",
                    "",
                )

            else:

                title = (
                    f"Recommendation {index}"
                )

                message = str(
                    rec_data
                )

                priority = ""

            with st.container(
                border=True
            ):

                rec_col1, rec_col2 = st.columns(
                    [4, 1],
                    gap="medium",
                )

                with rec_col1:

                    st.markdown(
                        f"**{title}**"
                    )

                    if message:

                        st.write(
                            message
                        )

                    st.caption(
                        rec_type.replace(
                            "_",
                            " ",
                        ).title()
                    )

                with rec_col2:

                    if priority:

                        priority_text = str(
                            priority
                        ).upper()

                        if priority_text == "HIGH":

                            st.error(
                                priority_text
                            )

                        elif priority_text == "MEDIUM":

                            st.warning(
                                priority_text
                            )

                        else:

                            st.info(
                                priority_text
                            )

    else:

        st.info(
            "No additional recommendations generated."
        )

    # =========================================================
    # PDF REPORT
    # =========================================================

    st.markdown("")
    st.divider()

    st.markdown("### 📄 ATS Report")

    st.caption(
        "Download the complete ATS analysis as a PDF."
    )

    if st.button(
        "📄 Generate ATS Report",
        use_container_width=True,
    ):

        with st.spinner(
            "Generating your ATS report..."
        ):

            report_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False,
                ) as temp_file:

                    report_path = temp_file.name

                generate_ats_report(
                    output_path=report_path,
                    ats_result=result.get(
                        "ats",
                        {},
                    ),
                    feedback=result.get(
                        "feedback",
                        {},
                    ),
                    recommendations=result.get(
                        "recommendations",
                        {},
                    ),
                    filename=filename,
                )

                with open(
                    report_path,
                    "rb",
                ) as pdf_file:

                    pdf_data = pdf_file.read()

                st.download_button(
                    label="📥 Download ATS Report",
                    data=pdf_data,
                    file_name="ATS_Resume_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

                st.success(
                    "✅ ATS report generated successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Failed to generate report: {e}"
                )

            finally:

                if (
                    report_path
                    and os.path.exists(report_path)
                ):

                    os.remove(
                        report_path
                    )