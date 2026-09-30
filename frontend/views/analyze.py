import textwrap
from html import escape

import streamlit as st

from frontend.components.analyze_styles import inject_analyze_styles
from frontend.services.api_client import analyze_resume
from backend.database.supabase_db import save_analysis


def html(content: str) -> str:
    """Remove Python indentation before rendering HTML."""
    return textwrap.dedent(content).strip()


# ============================================================
# DIALOG (replaces st.error)
# ============================================================

@st.dialog("Attention needed")
def _show_dialog(icon: str, title: str, message: str, items=None):
    """Styled popup used instead of st.error."""

    items_html = ""
    if items:
        rows = "".join(
            f'<div class="dlg-item"><span>✕</span>{escape(text)}</div>'
            for text in items
        )
        items_html = f'<div class="dlg-items">{rows}</div>'

    st.markdown(
        html(
            f"""
            <div class="dlg-body">
                <div class="dlg-icon">{icon}</div>
                <div class="dlg-title">{escape(title)}</div>
                <div class="dlg-text">{escape(message)}</div>
                {items_html}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    if st.button(
        "Got it",
        type="primary",
        use_container_width=True,
        key="dlg_close",
    ):
        st.rerun()


# ============================================================
# STYLES
# ============================================================

def _page_css():
    st.markdown(
        """
        <style>
            .an-hero { display: flex; align-items: center; gap: 16px; margin-bottom: 6px; }
            .an-hero-icon {
                width: 52px; height: 52px; border-radius: 14px;
                display: flex; align-items: center; justify-content: center;
                font-size: 26px;
                background: linear-gradient(135deg, #8B5CF6, #6366F1);
                box-shadow: 0 10px 28px rgba(99,102,241,0.35);
            }
            .an-title {
                font-size: 34px; font-weight: 800; color: #F8FAFC;
                letter-spacing: -0.8px; line-height: 1.1;
            }
            .an-title span { color: #A78BFA; }
            .an-subtitle { color: #94A3B8; font-size: 14.5px; margin: 8px 0 26px 0; }

            .an-step { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
            .an-step-num {
                width: 30px; height: 30px; border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-weight: 800; font-size: 14px; color: #FFFFFF;
                background: linear-gradient(135deg, #8B5CF6, #6366F1);
            }
            .an-step-title { font-size: 20px; font-weight: 750; color: #F8FAFC; }
            .an-step-hint { font-size: 12.5px; color: #64748B; margin: -6px 0 12px 42px; }

            .an-file {
                display: flex; align-items: center; gap: 12px; margin-top: 12px;
                padding: 12px 14px; border-radius: 12px;
                background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.30);
            }
            .an-file-icon { font-size: 22px; }
            .an-file-name {
                color: #E2E8F0; font-weight: 650; font-size: 14px;
                overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
            }
            .an-file-meta { color: #6EE7B7; font-size: 12px; }

            .an-ready { text-align: center; margin: 26px 0 10px 0; color: #64748B; font-size: 13px; }
            .an-ready b { color: #A78BFA; }

            .st-key-analyze_btn button {
                height: 54px !important; border-radius: 14px !important; font-size: 16px !important;
            }

            /* ---------- DIALOG ---------- */

            /* Dialog ka card: sab possible selectors */
            div[data-testid="stDialog"] [role="dialog"],
            div[role="dialog"],
            [data-testid="stModal"] > div,
            div[data-baseweb="modal"] [role="dialog"] {
                background: linear-gradient(145deg, #111827, #0F1424) !important;
                border: 1px solid rgba(139,92,246,0.35) !important;
                border-radius: 22px !important;
                box-shadow: 0 30px 80px rgba(0,0,0,0.55) !important;
            }

            /* Andar ke wrappers transparent rakho */
            div[role="dialog"] > div,
            div[role="dialog"] [data-testid="stVerticalBlock"],
            div[role="dialog"] [data-testid="stMarkdownContainer"] {
                background: transparent !important;
            }

            /* Dialog ka heading (Attention needed) */
            div[role="dialog"] h2,
            div[role="dialog"] [data-testid="stDialogTitle"] {
                color: #94A3B8 !important;
                font-size: 12px !important;
                font-weight: 700 !important;
                letter-spacing: 1.3px !important;
                text-transform: uppercase !important;
            }

            /* Close (X) button */
            div[role="dialog"] button[aria-label="Close"],
            div[role="dialog"] button[aria-label="Close"] svg {
                color: #94A3B8 !important;
                fill: #94A3B8 !important;
            }

            /* Overlay thoda dark */
            div[data-baseweb="modal"] > div:first-child {
                background: rgba(5,8,16,0.72) !important;
                backdrop-filter: blur(4px);
            }

            .dlg-body { text-align: center; padding: 6px 4px 14px 4px; }
            .dlg-icon {
                width: 64px; height: 64px; margin: 0 auto 14px; border-radius: 50%;
                display: flex; align-items: center; justify-content: center; font-size: 30px;
                background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.40);
                box-shadow: 0 0 30px rgba(239,68,68,0.20);
            }
            .dlg-title { font-size: 22px; font-weight: 800; color: #F8FAFC !important; margin-bottom: 8px; }
            .dlg-text { color: #94A3B8 !important; font-size: 14px; line-height: 1.7; }
            .dlg-items { margin-top: 16px; display: flex; flex-direction: column; gap: 8px; }
            .dlg-item {
                display: flex; align-items: center; gap: 10px; text-align: left;
                padding: 10px 14px; border-radius: 12px; font-size: 13.5px; font-weight: 600;
                background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.28);
                color: #FCA5A5 !important;
            }
            .dlg-item span { font-weight: 800; }

            .st-key-dlg_close button { height: 48px !important; border-radius: 12px !important; }
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


# ============================================================
# MAIN
# ============================================================

def render_analyze():
    """Render the Resume Analysis page."""

    inject_analyze_styles()
    _page_css()

    # ---------------- HEADER ----------------

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

    # ---------------- INPUTS ----------------

    resume_col, jd_col = st.columns(2, gap="large")

    with resume_col:

        _step_header(1, "Upload Resume", "PDF or DOCX, up to 5 MB")

        uploaded_resume = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            max_upload_size=5,
            label_visibility="collapsed",
            help="Supported formats: PDF and DOCX. Maximum size: 5 MB.",
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

    # ---------------- STATUS + BUTTON ----------------

    has_resume = uploaded_resume is not None
    has_job_description = bool(job_description.strip())

    if has_resume and has_job_description:
        st.markdown(
            '<div class="an-ready">Everything looks good. '
            'Click <b>Analyze Resume</b> to continue.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="an-ready">Upload your resume and enter '
            'a job description to continue.</div>',
            unsafe_allow_html=True,
        )

    _, btn_col, _ = st.columns([1, 2, 1])

    with btn_col:
        clicked = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
            key="analyze_btn",
        )

    if not clicked:
        return

    # ---------------- VALIDATION (dialog) ----------------

    missing = []
    if not has_resume:
        missing.append("Upload your resume (PDF or DOCX)")
    if not has_job_description:
        missing.append("Paste the job description")

    if missing:
        _show_dialog(
            icon="📋",
            title="Missing information",
            message="Please complete the following before starting the analysis.",
            items=missing,
        )
        return

    # ---------------- ANALYSIS ----------------

    error_message = None
    success = False

    with st.spinner("Analyzing your resume..."):

        try:

            result = analyze_resume(
                resume_file=uploaded_resume,
                job_description=job_description,
                use_groq=True,
            )

            st.session_state["analysis_result"] = result

            user = st.session_state.get("user")
            access_token = st.session_state.get("access_token")
            refresh_token = st.session_state.get("refresh_token")

            if not user or not access_token:
                error_message = (
                    "Your session has expired. "
                    "Please log in again and retry."
                )

            else:

                ats_data = result.get("ats", {})
                matching_data = result.get("matching", {})

                keyword_match = float(
                    ats_data.get("components", {}).get("required_skills", 0)
                )

                missing_list = [
                    skill.get("jd_skill", "")
                    for skill in matching_data.get("missing", [])
                    if skill.get("jd_skill")
                ]

                save_analysis(
                    user_id=str(user.id),
                    filename=uploaded_resume.name,
                    ats_score=float(ats_data.get("ats_score", 0)),
                    keyword_match=keyword_match,
                    missing_keywords=missing_list,
                    analysis_result=result,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                st.session_state["selected_history_analysis"] = {
                    "filename": uploaded_resume.name,
                    "ats_score": float(ats_data.get("ats_score", 0)),
                    "keyword_match": keyword_match,
                    "missing_keywords": missing_list,
                    "analysis_result": result,
                }

                st.session_state["current_page"] = "analysis_detail"
                success = True

        except Exception as e:
            error_message = str(e)

    # ---------------- RESULT ----------------

    if success:
        st.rerun()

    if error_message:
        _show_dialog(
            icon="⚠️",
            title="Analysis failed",
            message=error_message[:300],
        )