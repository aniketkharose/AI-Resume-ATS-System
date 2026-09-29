import textwrap
from html import escape

import streamlit as st

from frontend.components.analyze_styles import inject_analyze_styles
from frontend.services.api_client import analyze_resume
from backend.database.supabase_db import save_analysis


def html(content: str) -> str:
    """Remove Python indentation before rendering HTML."""
    return textwrap.dedent(content).strip()


def _page_css():
    st.markdown(
        """
        <style>
            .an-hero {
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 6px;
            }
            .an-hero-icon {
                width: 52px;
                height: 52px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                background: linear-gradient(135deg, #8B5CF6, #6366F1);
                box-shadow: 0 10px 28px rgba(99,102,241,0.35);
            }
            .an-title {
                font-size: 34px;
                font-weight: 800;
                color: #F8FAFC;
                letter-spacing: -0.8px;
                line-height: 1.1;
            }
            .an-title span { color: #A78BFA; }
            .an-subtitle {
                color: #94A3B8;
                font-size: 14.5px;
                margin: 8px 0 26px 0;
            }

            .an-step {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 14px;
            }
            .an-step-num {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 14px;
                color: #FFFFFF;
                background: linear-gradient(135deg, #8B5CF6, #6366F1);
            }
            .an-step-title {
                font-size: 20px;
                font-weight: 750;
                color: #F8FAFC;
            }
            .an-step-hint {
                font-size: 12.5px;
                color: #64748B;
                margin: -6px 0 12px 42px;
            }

            .an-file {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-top: 12px;
                padding: 12px 14px;
                border-radius: 12px;
                background: rgba(16,185,129,0.08);
                border: 1px solid rgba(16,185,129,0.30);
            }
            .an-file-icon { font-size: 22px; }
            .an-file-name {
                color: #E2E8F0;
                font-weight: 650;
                font-size: 14px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            .an-file-meta { color: #6EE7B7; font-size: 12px; }

            .an-ready {
                text-align: center;
                margin: 26px 0 10px 0;
                color: #64748B;
                font-size: 13px;
            }
            .an-ready b { color: #A78BFA; }

            /* Analyze button */
            .st-key-analyze_btn button {
                height: 54px !important;
                border-radius: 14px !important;
                font-size: 16px !important;
            }
            .st-key-analyze_btn button:disabled {
                opacity: 0.45 !important;
                cursor: not-allowed !important;
                transform: none !important;
                box-shadow: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _step_header(number: int, title: str, hint: str):
    st.markdown(
        html(
            f"""
            <div class="an-step">
                <div class="an-step-num">{number}</div>
                <div class="an-step-title">{title}</div>
            </div>
            <div class="an-step-hint">{hint}</div>
            """
        ),
        unsafe_allow_html=True,
    )


def render_analyze():
    """
    Render the Resume Analysis page.
    """

    inject_analyze_styles()
    _page_css()

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.markdown(
        html(
            """
            <div class="an-hero">
                <div class="an-hero-icon">📄</div>
                <div class="an-title">Analyze Your <span>Resume</span></div>
            </div>
            <div class="an-subtitle">
                Upload your resume and compare it with a target job description.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # =========================================================
    # INPUT SECTION
    # =========================================================

    resume_col, jd_col = st.columns(2, gap="large")

    # ---------------- RESUME UPLOAD ----------------

    with resume_col:

        _step_header(1, "Upload Resume", "PDF or DOCX, up to 5 MB")

        uploaded_resume = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            max_upload_size=5,
            label_visibility="collapsed",
            help=(
                "Supported formats: PDF and DOCX. "
                "Maximum size: 5 MB."
            ),
        )

        if uploaded_resume:

            file_size_mb = uploaded_resume.size / (1024 * 1024)

            st.markdown(
                html(
                    f"""
                    <div class="an-file">
                        <div class="an-file-icon">✅</div>
                        <div>
                            <div class="an-file-name">{escape(uploaded_resume.name)}</div>
                            <div class="an-file-meta">{file_size_mb:.2f} MB • Ready to analyze</div>
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

    # ---------------- JOB DESCRIPTION ----------------

    with jd_col:

        _step_header(2, "Job Description", "Paste the full job posting")

        job_description = st.text_area(
            "Paste the job description",
            label_visibility="collapsed",
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

    # =========================================================
    # ANALYZE BUTTON
    # =========================================================

    has_resume = uploaded_resume is not None
    has_job_description = bool(job_description.strip())

    # ---------------------------------------------------------
    # Status message
    # ---------------------------------------------------------

    if has_resume and has_job_description:

        st.markdown(
            '<div class="an-ready">'
            'Everything looks good. Click <b>Analyze Resume</b> to continue.'
            '</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<div class="an-ready">'
            'Upload your resume and enter a job description to continue.'
            '</div>',
            unsafe_allow_html=True,
        )


    # ---------------------------------------------------------
    # Analyze button
    # ---------------------------------------------------------

    _, btn_col, _ = st.columns([1, 2, 1])

    with btn_col:

        clicked = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
            key="analyze_btn",
        )


    # ---------------------------------------------------------
    # Button validation
    # ---------------------------------------------------------

    if clicked:

        # Resume missing
        if not has_resume:

            st.error(
                "📄 Please upload your resume before starting the analysis."
            )

        # Job description missing
        elif not has_job_description:

            st.error(
                "💼 Please enter the job description before starting the analysis."
            )

        # Everything is ready
        else:

            with st.spinner("Analyzing your resume..."):

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

                    st.session_state["analysis_result"] = result

                    # -------------------------------------------------
                    # SAVE RESULT TO SUPABASE
                    # -------------------------------------------------

                    user = st.session_state.get("user")
                    access_token = st.session_state.get("access_token")
                    refresh_token = st.session_state.get("refresh_token")

                    if not user:

                        st.warning(
                            "Analysis completed, "
                            "but no logged-in user was found."
                        )

                    elif not access_token:

                        st.warning(
                            "Analysis completed, "
                            "but authentication session was not found."
                        )

                    else:

                        ats_data = result.get("ats", {})
                        matching_data = result.get("matching", {})

                        save_analysis(
                            user_id=str(user.id),
                            filename=uploaded_resume.name,
                            ats_score=float(
                                ats_data.get("ats_score", 0)
                            ),
                            keyword_match=float(
                                ats_data.get("components", {}).get(
                                    "required_skills", 0
                                )
                            ),
                            missing_keywords=[
                                skill.get("jd_skill", "")
                                for skill in matching_data.get("missing", [])
                                if skill.get("jd_skill")
                            ],
                            analysis_result=result,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )

                        missing_list = [
                            skill.get("jd_skill", "")
                            for skill in matching_data.get("missing", [])
                            if skill.get("jd_skill")
                        ]

                        st.session_state["selected_history_analysis"] = {
                            "filename": uploaded_resume.name,
                            "ats_score": float(
                                ats_data.get("ats_score", 0)
                            ),
                            "keyword_match": float(
                                ats_data.get("components", {}).get(
                                    "required_skills", 0
                                )
                            ),
                            "missing_keywords": missing_list,
                            "analysis_result": result,
                        }

                        st.session_state["current_page"] = "analysis_detail"

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Analysis failed: {e}"
                    )

        with st.spinner("Analyzing your resume..."):

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

                st.session_state["analysis_result"] = result

                # -------------------------------------------------
                # SAVE RESULT TO SUPABASE
                # -------------------------------------------------

                user = st.session_state.get("user")
                access_token = st.session_state.get("access_token")
                refresh_token = st.session_state.get("refresh_token")

                if not user:

                    st.warning(
                        "Analysis completed, "
                        "but no logged-in user was found."
                    )

                elif not access_token:

                    st.warning(
                        "Analysis completed, "
                        "but authentication session was not found."
                    )

                else:

                    ats_data = result.get("ats", {})
                    matching_data = result.get("matching", {})

                    save_analysis(
                        user_id=str(user.id),
                        filename=uploaded_resume.name,
                        ats_score=float(
                            ats_data.get("ats_score", 0)
                        ),
                        keyword_match=float(
                            ats_data.get("components", {}).get(
                                "required_skills", 0
                            )
                        ),
                        missing_keywords=[
                            skill.get("jd_skill", "")
                            for skill in matching_data.get("missing", [])
                            if skill.get("jd_skill")
                        ],
                        analysis_result=result,
                        access_token=access_token,
                        refresh_token=refresh_token,
                    )

                    missing_list = [
                        skill.get("jd_skill", "")
                        for skill in matching_data.get("missing", [])
                        if skill.get("jd_skill")
                    ]

                    st.session_state["selected_history_analysis"] = {
                        "filename": uploaded_resume.name,
                        "ats_score": float(ats_data.get("ats_score", 0)),
                        "keyword_match": float(
                            ats_data.get("components", {}).get("required_skills", 0)
                        ),
                        "missing_keywords": missing_list,
                        "analysis_result": result,
                    }

                    st.session_state["current_page"] = "analysis_detail"
                    st.rerun()

            except Exception as e:

                st.error(f"❌ Analysis failed: {e}")