import streamlit as st
from datetime import datetime

from backend.database.supabase_db import get_user_analyses


def render_history():
    """
    Render the user's resume analysis history.
    """

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.title("📊 Analysis History")

    st.caption(
        "View your previous resume analyses and ATS results."
    )

    st.divider()

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    user = st.session_state.get("user")

    access_token = st.session_state.get(
        "access_token"
    )

    refresh_token = st.session_state.get(
        "refresh_token"
    )

    if not user:
        st.warning(
            "Please log in to view your analysis history."
        )
        return

    if not access_token or not refresh_token:
        st.warning(
            "Your authentication session is missing. "
            "Please log in again."
        )
        return

    # =========================================================
    # FETCH HISTORY
    # =========================================================

    try:

        history = get_user_analyses(
            user_id=str(user.id),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except Exception as e:

        st.error(
            f"❌ Failed to load analysis history: {e}"
        )

        return

    # =========================================================
    # EMPTY STATE
    # =========================================================

    if not history:

        st.info(
            "📄 No analysis history yet. "
            "Analyze your first resume to see it here."
        )

        return

    # =========================================================
    # SUMMARY STATISTICS
    # =========================================================

    total_analyses = len(history)

    average_score = (
        sum(
            float(item.get("ats_score", 0))
            for item in history
        )
        / total_analyses
    )

    latest_score = float(
        history[0].get("ats_score", 0)
    )

    stat1, stat2, stat3 = st.columns(
        3,
        gap="medium",
    )

    with stat1:

        st.metric(
            label="Total Analyses",
            value=total_analyses,
        )

    with stat2:

        st.metric(
            label="Average ATS Score",
            value=f"{average_score:.1f}",
        )

    with stat3:

        st.metric(
            label="Latest ATS Score",
            value=f"{latest_score:.1f}",
        )

    # =========================================================
    # PREVIOUS ANALYSES
    # =========================================================

    st.markdown("")
    st.subheader("📋 Previous Analyses")

    # =========================================================
    # HISTORY CARDS
    # =========================================================

    for item in history:

        filename = item.get(
            "filename",
            "Unknown Resume",
        )

        ats_score = float(
            item.get("ats_score", 0)
        )

        keyword_match = float(
            item.get("keyword_match", 0)
        )

        missing_keywords = item.get(
            "missing_keywords",
            [],
        )

        created_at = item.get(
            "created_at",
            "",
        )

        # -----------------------------------------------------
        # DATE FORMAT
        # -----------------------------------------------------

        formatted_date = created_at

        if created_at:

            try:

                date_object = datetime.fromisoformat(
                    created_at.replace(
                        "Z",
                        "+00:00",
                    )
                )

                formatted_date = date_object.strftime(
                    "%d %b %Y • %I:%M %p"
                )

            except Exception:

                pass

        # -----------------------------------------------------
        # SCORE STATUS
        # -----------------------------------------------------

        if ats_score >= 80:

            score_status = "Strong"
            score_icon = "🟢"

        elif ats_score >= 60:

            score_status = "Moderate"
            score_icon = "🟡"

        else:

            score_status = "Needs Improvement"
            score_icon = "🔴"

        # -----------------------------------------------------
        # CARD
        # -----------------------------------------------------

        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1],
                gap="large",
            )

            # -------------------------------------------------
            # LEFT SIDE
            # -------------------------------------------------

            with col1:

                st.markdown(
                    f"### 📄 {filename}"
                )

                st.caption(
                    f"Analyzed on {formatted_date}"
                )

                st.markdown(
                    f"{score_icon} **{score_status}**"
                )

                if missing_keywords:

                    missing_text = ", ".join(
                        str(skill)
                        for skill in missing_keywords
                    )

                    st.caption(
                        f"Missing skills: {missing_text}"
                    )

                else:

                    st.caption(
                        "No missing skills recorded."
                    )

            # -------------------------------------------------
            # RIGHT SIDE — ATS SCORE
            # -------------------------------------------------

            with col2:

                st.metric(
                    label="ATS Score",
                    value=f"{ats_score:.0f}/100",
                )

            # -------------------------------------------------
            # KEYWORD MATCH
            # -------------------------------------------------

            st.progress(
                min(
                    max(keyword_match / 100, 0.0),
                    1.0,
                ),
                text=(
                    f"Keyword Match: "
                    f"{keyword_match:.0f}%"
                ),
            )

            # -------------------------------------------------
            # VIEW ANALYSIS
            # -------------------------------------------------

            if st.button(
                "View Analysis",
                key=f"view_analysis_{item.get('id')}",
                use_container_width=True,
            ):

                st.session_state[
                    "selected_history_analysis"
                ] = item

                st.session_state[
                    "current_page"
                ] = "analysis_detail"

                st.rerun()