import streamlit as st

from frontend.services.api_client import analyze_resume
from backend.database.supabase_db import save_analysis


def render_analyze():
    """
    Render the Resume Analysis page.
    """

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.title("📄 Analyze Your Resume")

    st.caption(
        "Upload your resume and compare it with a target job description."
    )

    st.divider()

    # =========================================================
    # INPUT SECTION
    # =========================================================

    resume_col, jd_col = st.columns(
        2,
        gap="large",
    )

    # =========================================================
    # RESUME UPLOAD
    # =========================================================

    with resume_col:

        st.markdown("### 📄 Resume")

        uploaded_resume = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            max_upload_size=5,
            help=(
                "Supported formats: PDF and DOCX. "
                "Maximum size: 5 MB."
            ),
        )

        if uploaded_resume:

            file_size_mb = (
                uploaded_resume.size
                / (1024 * 1024)
            )

            st.success(
                f"✅ {uploaded_resume.name} "
                f"• {file_size_mb:.2f} MB"
            )

    # =========================================================
    # JOB DESCRIPTION
    # =========================================================

    with jd_col:

        st.markdown("### 💼 Job Description")

        job_description = st.text_area(
            "Paste the job description",
            placeholder=(
                "Example:\n\n"
                "We are looking for an AI/ML Engineer "
                "with experience in Python, Machine Learning, "
                "Deep Learning, NLP, TensorFlow, PyTorch "
                "and FastAPI..."
            ),
            height=250,
        )

    # =========================================================
    # ANALYZE BUTTON
    # =========================================================

    st.markdown("")

    if uploaded_resume and job_description.strip():

        if st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
        ):

            with st.spinner(
                "Analyzing your resume..."
            ):

                try:

                    # -------------------------------------------------
                    # CALL FASTAPI
                    # -------------------------------------------------

                    result = analyze_resume(
                        resume_file=uploaded_resume,
                        job_description=job_description,
                        use_groq=True,
                    )

                    # -------------------------------------------------
                    # SAVE RESULT IN SESSION
                    # -------------------------------------------------

                    st.session_state[
                        "analysis_result"
                    ] = result

                    # -------------------------------------------------
                    # SAVE RESULT TO SUPABASE
                    # -------------------------------------------------

                    user = st.session_state.get(
                        "user"
                    )

                    access_token = (
                        st.session_state.get(
                            "access_token"
                        )
                    )

                    refresh_token = (
                        st.session_state.get(
                            "refresh_token"
                        )
                    )

                    if not user:

                        st.warning(
                            "Analysis completed, "
                            "but no logged-in user was found."
                        )

                    elif not access_token:

                        st.warning(
                            "Analysis completed, "
                            "but authentication session "
                            "was not found."
                        )

                    else:

                        ats_data = result.get(
                            "ats",
                            {},
                        )

                        matching_data = result.get(
                            "matching",
                            {},
                        )

                        save_analysis(
                            user_id=str(
                                user.id
                            ),
                            filename=(
                                uploaded_resume.name
                            ),
                            ats_score=float(
                                ats_data.get(
                                    "ats_score",
                                    0,
                                )
                            ),
                            keyword_match=float(
                                ats_data.get(
                                    "components",
                                    {},
                                ).get(
                                    "required_skills",
                                    0,
                                )
                            ),
                            missing_keywords=[
                                skill.get(
                                    "jd_skill",
                                    "",
                                )
                                for skill in (
                                    matching_data.get(
                                        "missing",
                                        [],
                                    )
                                )
                                if skill.get(
                                    "jd_skill"
                                )
                            ],
                            analysis_result=result,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )

                        st.success(
                            "✅ Resume analyzed "
                            "and saved successfully!"
                        )

                except Exception as e:

                    st.error(
                        f"❌ Analysis failed: {e}"
                    )

    else:

        st.caption(
            "Upload your resume and enter a "
            "job description to continue."
        )