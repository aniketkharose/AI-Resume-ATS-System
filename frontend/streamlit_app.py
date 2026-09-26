import streamlit as st
import tempfile
import os
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# FRONTEND SERVICES
# ============================================================

from services.supabase_client import (
    get_supabase_client,
    sign_up_user,
    login_user,
    logout_user,
)

from services.api_client import analyze_resume


# ============================================================
# BACKEND SERVICES
# ============================================================

from backend.database.supabase_db import get_user_analyses
from backend.services.report_generator import generate_ats_report
from views.history import render_history
from views.analysis_detail import render_analysis_detail

# ============================================================
# AUTHENTICATION STATE
# ============================================================

if "user" not in st.session_state:
    st.session_state["user"] = None

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None

if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "login"

# ============================================================
# PAGE STATE
# ============================================================

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# ============================================================
# AUTHENTICATION UI
# ============================================================

if st.session_state["user"] is None:

    st.markdown("## 🧠 AI Resume ATS")

    st.caption(
        "Sign in to analyze your resume and save analysis history."
    )

    # --------------------------------------------------------
    # LOGIN / SIGNUP TABS
    # --------------------------------------------------------

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.markdown("### Welcome back")

        login_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary",
        ):

            if not login_email.strip():

                st.error("Please enter your email.")

            elif not login_password:

                st.error("Please enter your password.")

            else:

                try:

                    response = login_user(
                        login_email,
                        login_password,
                    )

                    if response.user and response.session:

                        st.session_state["user"] = response.user

                        # Save Supabase authentication tokens
                        st.session_state["access_token"] = response.session.access_token
                        st.session_state["refresh_token"] = response.session.refresh_token

                        st.success(
                            "✅ Login successful!"
                        )

                        st.rerun()


                    else:

                        st.error(
                            "Login failed. Please check your credentials."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Login failed: {e}"
                    )

    # ========================================================
    # SIGN UP
    # ========================================================

    with signup_tab:

        st.markdown("### Create your account")

        signup_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="signup_email",
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="signup_password",
        )

        signup_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            type="primary",
        ):

            if not signup_email.strip():

                st.error("Please enter your email.")

            elif len(signup_password) < 8:

                st.error(
                    "Password must contain at least 8 characters."
                )

            elif signup_password != signup_confirm:

                st.error(
                    "Passwords do not match."
                )

            else:

                try:

                    response = sign_up_user(
                        signup_email,
                        signup_password,
                    )

                    if response.user:

                        st.session_state["user"] = response.user

                        # Save Supabase session if available
                        if response.session:
                            st.session_state["access_token"] = response.session.access_token
                            st.session_state["refresh_token"] = response.session.refresh_token

                            st.success(
                                "✅ Account created successfully!"
                            )

                            st.rerun()

                        else:
                            st.success(
                                "✅ Account created successfully!"
                            )

                            st.info(
                                "Please check your email and confirm "
                                "your account before logging in."
                            )

                    else:

                        st.error(
                            "Account creation failed."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Signup failed: {e}"
                    )

    # --------------------------------------------------------
    # STOP HERE
    # --------------------------------------------------------

    st.stop()
    
    
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume ATS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown("## 🧠 AI Resume ATS")

    st.markdown("---")

    if st.button(
        "🏠 Home",
        use_container_width=True,
    ):
        st.session_state["current_page"] = "home"
        st.rerun()

    if st.button(
        "📊 Analysis History",
        use_container_width=True,
    ):
        st.session_state["current_page"] = "history"
        st.rerun()

    st.markdown("---")

    user = st.session_state.get("user")

    if user:
        st.caption(
            f"Signed in as\n{user.email}"
        )

# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state["current_page"] == "history":

    render_history()

    st.stop()


if st.session_state["current_page"] == "analysis_detail":

    render_analysis_detail()

    st.stop()

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #0b0f19;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Header ---------- */

    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0 25px 0;
    }

    .brand {
        font-size: 1.45rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .brand span {
        color: #7c3aed;
    }

    .header-badge {
        display: inline-block;
        padding: 7px 14px;
        border: 1px solid rgba(124, 58, 237, 0.35);
        border-radius: 999px;
        background: rgba(124, 58, 237, 0.10);
        color: #c4b5fd;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ---------- Hero ---------- */

    .hero {
        text-align: center;
        padding: 75px 20px 55px 20px;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.30);
        color: #c4b5fd;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: 4rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0;
        color: #ffffff;
    }

    .hero h1 span {
        color: #8b5cf6;
    }

    .hero p {
        max-width: 720px;
        margin: 22px auto 0 auto;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #94a3b8;
    }

    /* ---------- Feature Cards ---------- */

    .feature-card {
        height: 100%;
        padding: 25px;
        border-radius: 18px;
        background: #111827;
        border: 1px solid #1f2937;
        transition: 0.2s ease;
    }

    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 14px;
    }

    .feature-title {
        color: #f8fafc;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ---------- Section ---------- */

    .section-title {
        text-align: center;
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 750;
        margin-top: 65px;
        margin-bottom: 28px;
    }

    .section-subtitle {
        text-align: center;
        color: #64748b;
        margin-top: -18px;
        margin-bottom: 30px;
    }

    /* ---------- Bottom CTA ---------- */

    .cta-box {
        margin-top: 65px;
        padding: 35px;
        text-align: center;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.15),
            rgba(59, 130, 246, 0.08)
        );
        border: 1px solid rgba(124, 58, 237, 0.25);
    }

    .cta-title {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
    }

    .cta-text {
        color: #94a3b8;
        margin-top: 8px;
    }

    /* ---------- Hide Streamlit Menu ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="app-header">
        <div class="brand">🧠 AI Resume <span>ATS</span></div>
        <div class="header-badge">AI-Powered Resume Analysis</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-badge">✨ Resume Intelligence Platform</div>
    <h1>Make Your Resume<br><span>Job-Ready.</span></h1>
    <p>
        Analyze your resume against a job description using
        skill matching, semantic similarity and ATS scoring —
        then get actionable recommendations to improve your resume.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# FEATURES
# ============================================================

st.markdown(
    '<div class="section-title">Everything You Need to Optimize Your Resume</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">One platform. Complete resume intelligence.</div>',
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns(3, gap="large")


with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">ATS Score</div>
            <div class="feature-text">
                Get a structured ATS compatibility score based on
                skills, relevance, resume structure and content.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Skill Matching</div>
            <div class="feature-text">
                Identify required, preferred, matched and missing
                skills from the target job description.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Smart Recommendations</div>
            <div class="feature-text">
                Receive practical recommendations to improve your
                resume without adding skills you don't actually have.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ANALYSIS PIPELINE PREVIEW
# ============================================================

st.markdown(
    '<div class="section-title">How It Works</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">From resume upload to actionable insights.</div>',
    unsafe_allow_html=True,
)


step1, step2, step3, step4 = st.columns(4, gap="medium")


with step1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">1. Upload</div>
            <div class="feature-text">
                Upload your resume in PDF or DOCX format.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with step2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">2. Analyze</div>
            <div class="feature-text">
                Extract skills, sections and resume information.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with step3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">3. Match</div>
            <div class="feature-text">
                Compare your resume with the target job description.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with step4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">4. Improve</div>
            <div class="feature-text">
                Get an ATS score, feedback and improvement suggestions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CTA
# ============================================================

st.markdown(
    """
<div class="cta-box">
    <div class="cta-title">Ready to analyze your resume?</div>
    <div class="cta-text">
        Resume upload and job description analysis will be available here.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# RESUME ANALYSIS INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Analyze Your Resume</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Upload your resume and paste the target job description.</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")


# ------------------------------------------------------------
# RESUME UPLOAD
# ------------------------------------------------------------

with col1:
    st.markdown("### 📄 Resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        max_upload_size=5,
        help="Supported formats: PDF and DOCX. Maximum size: 5 MB.",
    )

    if uploaded_resume:
        file_size_mb = uploaded_resume.size / (1024 * 1024)

        st.success(
            f"✅ {uploaded_resume.name} • {file_size_mb:.2f} MB"
        )


# ------------------------------------------------------------
# JOB DESCRIPTION
# ------------------------------------------------------------

with col2:
    st.markdown("### 💼 Job Description")

    job_description = st.text_area(
        "Paste the job description",
        placeholder=(
            "Example:\n\n"
            "We are looking for an AI/ML Engineer with experience "
            "in Python, Machine Learning, Deep Learning, NLP, "
            "TensorFlow, PyTorch and FastAPI..."
        ),
        height=250,
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

if uploaded_resume and job_description.strip():

    if st.button(
        "🚀 Analyze Resume",
        use_container_width=True,
        type="primary",
    ):

        with st.spinner("Analyzing your resume..."):

            try:

                # Send resume + job description to FastAPI
                result = analyze_resume(
                    resume_file=uploaded_resume,
                    job_description=job_description,
                    use_groq=True,
                )

                # Save analysis result in Streamlit session
                st.session_state["analysis_result"] = result

                # --------------------------------------------------------
                # SAVE ANALYSIS TO SUPABASE
                # --------------------------------------------------------

                try:
                    from backend.database.supabase_db import save_analysis

                    user = st.session_state.get("user")

                    if not user:
                        st.warning(
                            "Analysis completed, but no logged-in user was found."
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
                            # Authenticated Supabase session
                            access_token=st.session_state.get("access_token"),
                            refresh_token=st.session_state.get("refresh_token"),
                        )

                        st.success(
                            "✅ Resume analyzed and saved to your history!"
                        )

                except Exception as save_error:

                    st.warning(
                        f"⚠️ Analysis completed, but history save failed: {save_error}"
                    )

            except Exception as e:

                st.error(f"❌ Analysis failed: {e}")

else:

    st.caption(
        "Upload your resume and enter a job description to continue."
    )



# ============================================================
# ATS SCORE RESULT
# ============================================================

result = st.session_state.get("analysis_result")

if result:

    ats_data = result.get("ats", {})
    ats_score = ats_data.get("ats_score", 0)

    score_html = f"""
<div style="margin-top:45px; padding:35px; border-radius:22px; background:#111827; border:1px solid #1f2937; text-align:center;">
<div style="color:#94a3b8; font-size:0.9rem; font-weight:600; text-transform:uppercase; letter-spacing:1.5px;">YOUR ATS SCORE</div>
<div style="margin-top:10px; font-size:4.5rem; font-weight:800; color:#a78bfa; line-height:1;">{ats_score:.1f}</div>
<div style="margin-top:8px; color:#64748b; font-size:0.95rem;">out of 100</div>
</div>
"""

    st.markdown(score_html, unsafe_allow_html=True)


# ============================================================
# ATS SCORE BREAKDOWN
# ============================================================

if result:

    components = ats_data.get("components", {})

    required_score = components.get("required_skills", 0)
    preferred_score = components.get("preferred_skills", 0)
    semantic_score = components.get("semantic_relevance", 0)
    structure_score = components.get("resume_structure", 0)
    completeness_score = components.get("content_completeness", 0)

    st.markdown(
        "<h2 style='text-align:center; color:#f8fafc; "
        "font-size:1.6rem; margin-top:35px; margin-bottom:8px;'>"
        "ATS Score Breakdown</h2>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align:center; color:#64748b; "
        "font-size:0.9rem; margin-bottom:25px;'>"
        "See how your resume performed across each ATS dimension."
        "</p>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # BREAKDOWN CARDS
    # --------------------------------------------------------

    card1, card2, card3 = st.columns(3, gap="medium")

    with card1:
        st.markdown(
            f"""
<div style="
    background:#111827;
    border:1px solid #1f2937;
    border-radius:16px;
    padding:22px;
    text-align:center;
">
    <div style="font-size:1.5rem;">🎯</div>
    <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
        Required Skills
    </div>
    <div style="color:#a78bfa; font-size:2rem; font-weight:800; margin-top:6px;">
        {required_score:.0f}%
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with card2:
        st.markdown(
            f"""
<div style="
    background:#111827;
    border:1px solid #1f2937;
    border-radius:16px;
    padding:22px;
    text-align:center;
">
    <div style="font-size:1.5rem;">⭐</div>
    <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
        Preferred Skills
    </div>
    <div style="color:#a78bfa; font-size:2rem; font-weight:800; margin-top:6px;">
        {preferred_score:.0f}%
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with card3:
        st.markdown(
            f"""
<div style="
    background:#111827;
    border:1px solid #1f2937;
    border-radius:16px;
    padding:22px;
    text-align:center;
">
    <div style="font-size:1.5rem;">🧠</div>
    <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
        Semantic Relevance
    </div>
    <div style="color:#a78bfa; font-size:2rem; font-weight:800; margin-top:6px;">
        {semantic_score:.0f}%
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # SECOND ROW
    # --------------------------------------------------------

    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)

    card4, card5 = st.columns(2, gap="medium")

    with card4:
        st.markdown(
            f"""
<div style="
    background:#111827;
    border:1px solid #1f2937;
    border-radius:16px;
    padding:22px;
    text-align:center;
">
    <div style="font-size:1.5rem;">📄</div>
    <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
        Resume Structure
    </div>
    <div style="color:#a78bfa; font-size:2rem; font-weight:800; margin-top:6px;">
        {structure_score:.0f}%
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with card5:
        st.markdown(
            f"""
<div style="
    background:#111827;
    border:1px solid #1f2937;
    border-radius:16px;
    padding:22px;
    text-align:center;
">
    <div style="font-size:1.5rem;">📝</div>
    <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
        Content Completeness
    </div>
    <div style="color:#a78bfa; font-size:2rem; font-weight:800; margin-top:6px;">
        {completeness_score:.0f}%
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

# ============================================================
# SKILL MATCHING
# ============================================================

if result:

    matching_data = result.get("matching", {})

    matched_skills = matching_data.get("matched", [])
    related_skills = matching_data.get("related", [])
    missing_skills = matching_data.get("missing", [])

    # --------------------------------------------------------
    # SECTION HEADER
    # --------------------------------------------------------

    st.markdown("")
    st.markdown("## 🎯 Skill Matching")

    st.caption(
        "See how your resume matches the target job description."
    )

    # --------------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------------

    st.markdown("### 🟢 Matched Skills")

    if matched_skills:

        # Display skills in 3-column grid
        for i in range(0, len(matched_skills), 3):

            row_skills = matched_skills[i:i + 3]

            columns = st.columns(3, gap="medium")

            for column, skill in zip(columns, row_skills):

                skill_name = skill.get(
                    "jd_skill",
                    "Unknown",
                )

                category = skill.get(
                    "category",
                    "Unknown",
                )

                importance = skill.get(
                    "importance",
                    "general",
                )

                match_type = skill.get(
                    "match_type",
                    "exact",
                )

                with column:

                    with st.container(border=True):

                        st.markdown(
                            f"**{skill_name}**"
                        )

                        st.caption(category)

                        if importance == "required":
                            st.success(
                                f"Required • {match_type.title()}"
                            )

                        elif importance == "preferred":
                            st.info(
                                f"Preferred • {match_type.title()}"
                            )

                        else:
                            st.caption(
                                f"General • {match_type.title()}"
                            )

    else:

        st.info("No matched skills found.")

    # --------------------------------------------------------
    # RELATED SKILLS
    # --------------------------------------------------------

    if related_skills:

        st.markdown("### 🟡 Related Skills")

        for i in range(0, len(related_skills), 2):

            row_skills = related_skills[i:i + 2]

            columns = st.columns(2, gap="medium")

            for column, skill in zip(columns, row_skills):

                jd_skill = skill.get(
                    "jd_skill",
                    "Unknown",
                )

                resume_skill = skill.get(
                    "resume_skill",
                    "Unknown",
                )

                similarity = skill.get(
                    "similarity",
                    0,
                )

                with column:

                    with st.container(border=True):

                        st.markdown(
                            f"**{jd_skill}**"
                        )

                        st.caption(
                            f"Resume skill: {resume_skill}"
                        )

                        st.progress(
                            min(float(similarity), 1.0),
                            text=f"{similarity * 100:.1f}% semantic similarity",
                        )

    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    st.markdown("### 🔴 Missing Skills")

    if missing_skills:

        for skill in missing_skills:

            skill_name = skill.get(
                "jd_skill",
                "Unknown",
            )

            category = skill.get(
                "category",
                "Unknown",
            )

            importance = skill.get(
                "importance",
                "general",
            )

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1],
                    gap="medium",
                )

                with col1:

                    st.markdown(
                        f"**{skill_name}**"
                    )

                    st.caption(category)

                with col2:

                    if importance == "required":

                        st.error("REQUIRED")

                    elif importance == "preferred":

                        st.warning("PREFERRED")

                    else:

                        st.caption("GENERAL")

    else:

        st.success(
            "🎉 No missing skills detected!"
        )

# ============================================================
# FEEDBACK & RECOMMENDATIONS
# ============================================================

if result:

    feedback_data = result.get("feedback", {})
    recommendation_data = result.get("recommendations", {})

    # ========================================================
    # FEEDBACK
    # ========================================================

    st.markdown("")
    st.markdown("## 💡 Resume Feedback")

    st.caption(
        "Understand what is working well and what you can improve."
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = feedback_data.get(
        "summary",
        "No summary available."
    )

    st.markdown("### 📋 Overall Summary")

    with st.container(border=True):
        st.write(summary)

    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    strengths = feedback_data.get(
        "strengths",
        []
    )

    st.markdown("### 🟢 Strengths")

    if strengths:

        for strength in strengths:

            if isinstance(strength, dict):

                title = strength.get(
                    "title",
                    strength.get("message", "Strength")
                )

                description = strength.get(
                    "description",
                    ""
                )

                st.success(
                    f"**{title}**\n\n{description}"
                )

            else:

                st.success(strength)

    else:

        st.info("No specific strengths identified.")

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    improvements = feedback_data.get(
        "improvements",
        []
    )

    st.markdown("### ⚠️ Improvements")

    if improvements:

        for improvement in improvements:

            if isinstance(improvement, dict):

                title = improvement.get(
                    "title",
                    improvement.get("message", "Improvement")
                )

                description = improvement.get(
                    "description",
                    ""
                )

                st.warning(
                    f"**{title}**\n\n{description}"
                )

            else:

                st.warning(str(improvement))

    else:

        st.info("No specific improvements identified.")

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown("")
    st.markdown("## 🚀 Recommendations")

    st.caption(
        "Actionable suggestions to improve your resume for the target role."
    )

    # --------------------------------------------------------
    # HANDLE RECOMMENDATION DATA
    # --------------------------------------------------------

    if isinstance(recommendation_data, dict):

        all_recommendations = []

        for key, items in recommendation_data.items():

            if isinstance(items, list):

                for item in items:

                    if isinstance(item, dict):

                        all_recommendations.append({
                            "type": key,
                            "data": item,
                        })

                    else:

                        all_recommendations.append({
                            "type": key,
                            "data": str(item),
                        })

    elif isinstance(recommendation_data, list):

        all_recommendations = [
            {
                "type": "recommendation",
                "data": item,
            }
            for item in recommendation_data
        ]

    else:

        all_recommendations = []

    # --------------------------------------------------------
    # DISPLAY RECOMMENDATIONS
    # --------------------------------------------------------

    if all_recommendations:

        for index, recommendation in enumerate(
            all_recommendations,
            start=1,
        ):

            rec_type = recommendation["type"]
            rec_data = recommendation["data"]

            if isinstance(rec_data, dict):

                title = rec_data.get(
                    "skill",
                    rec_data.get(
                        "title",
                        f"Recommendation {index}"
                    ),
                )

                message = rec_data.get(
                    "message",
                    rec_data.get(
                        "recommendation",
                        rec_data.get(
                            "description",
                            ""
                        ),
                    ),
                )

                priority = rec_data.get(
                    "priority",
                    "",
                )

            else:

                title = f"Recommendation {index}"
                message = str(rec_data)
                priority = ""

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1],
                    gap="medium",
                )

                with col1:

                    st.markdown(
                        f"**{title}**"
                    )

                    if message:
                        st.write(message)

                    st.caption(
                        rec_type.replace(
                            "_",
                            " "
                        ).title()
                    )

                with col2:

                    if priority:

                        if str(priority).lower() == "high":

                            st.error(
                                str(priority).upper()
                            )

                        elif str(priority).lower() == "medium":

                            st.warning(
                                str(priority).upper()
                            )

                        else:

                            st.info(
                                str(priority).upper()
                            )

    else:

        st.info(
            "No additional recommendations generated."
        )


# ============================================================
# PDF REPORT DOWNLOAD
# ============================================================

if result:

    st.markdown("")
    st.markdown("---")
    st.markdown("## 📄 ATS Report")

    st.caption(
        "Download a complete PDF report containing your ATS score, "
        "skill analysis, feedback and recommendations."
    )

    if st.button(
        "📄 Generate ATS Report",
        use_container_width=True,
    ):

        with st.spinner("Generating your ATS report..."):

            try:

                # Create temporary PDF file
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False,
                ) as temp_file:

                    report_path = temp_file.name

                # Generate report using existing backend service
                generate_ats_report(
                    output_path=report_path,
                    ats_result=result.get("ats", {}),
                    feedback=result.get("feedback", {}),
                    recommendations=result.get(
                        "recommendations",
                        {},
                    ),
                    filename=uploaded_resume.name,
                )

                # Read generated PDF
                with open(
                    report_path,
                    "rb",
                ) as pdf_file:

                    pdf_data = pdf_file.read()

                # Download button
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

                # Remove temporary file
                os.remove(report_path)

            except Exception as e:

                st.error(
                    f"❌ Failed to generate report: {e}"
                )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:45px;
        color:#475569;
        font-size:0.8rem;
    ">
        AI Resume ATS • Built with FastAPI + Streamlit + NLP
    </div>
    """,
    unsafe_allow_html=True,
)