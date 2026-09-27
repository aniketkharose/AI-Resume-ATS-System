import streamlit as st


def render_home():

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
<div class="app-header">
    <div class="brand">🧠 AI Resume <span>ATS</span></div>
    <div class="header-badge">AI-Powered Resume Analysis</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ========================================================
    # HERO
    # ========================================================
    st.markdown(
        '<div class="hero-badge">✨ Resume Intelligence Platform</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    # Make Your Resume
    # <span style="color:#8b5cf6;">Job-Ready.</span>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    Analyze your resume against a job description using
    skill matching, semantic similarity and ATS scoring —
    then get actionable recommendations to improve your resume.
    """
    )

    # ========================================================
    # FEATURES
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Everything You Need to Optimize Your Resume'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'One platform. Complete resume intelligence.'
        '</div>',
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

    # ========================================================
    # HOW IT WORKS
    # ========================================================

    st.markdown(
        '<div class="section-title">How It Works</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'From resume upload to actionable insights.'
        '</div>',
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

    # ========================================================
    # CTA
    # ========================================================

    st.markdown(
        """
<div class="cta-box">
    <div class="cta-title">Ready to analyze your resume?</div>

    <div class="cta-text">
        Upload your resume and compare it with your target
        job description to get actionable insights.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ========================================================
    # FOOTER
    # ========================================================

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