import streamlit as st


def render_home():

    # ========================================================
    # PREMIUM HOME PAGE CSS
    # ========================================================

    st.markdown(
        """
        <style>

        /* ---------- GLOBAL ---------- */

        .home-wrapper {
            max-width: 1180px;
            margin: 0 auto;
        }


        /* ---------- HERO ---------- */

        .hero-shell {
            padding: 52px 48px;
            border-radius: 30px;
            border: 1px solid rgba(139, 92, 246, 0.25);

            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(139, 92, 246, 0.22),
                    transparent 32%
                ),
                radial-gradient(
                    circle at 10% 90%,
                    rgba(99, 102, 241, 0.12),
                    transparent 35%
                ),
                #0F1422;

            box-shadow:
                0 30px 80px rgba(0, 0, 0, 0.35);
        }


        .hero-grid {
            display: grid;
            grid-template-columns: 1.45fr 0.75fr;
            gap: 42px;
            align-items: center;
        }


        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 7px;

            padding: 8px 14px;
            margin-bottom: 20px;

            border-radius: 999px;

            background: rgba(139, 92, 246, 0.10);
            border: 1px solid rgba(139, 92, 246, 0.25);

            color: #C4B5FD;

            font-size: 13px;
            font-weight: 650;
        }


        .hero-title {
            color: #F8FAFC;

            font-size: 58px;
            line-height: 1.04;

            font-weight: 850;
            letter-spacing: -2.8px;

            margin-bottom: 22px;
        }


        .hero-gradient {
            background:
                linear-gradient(
                    90deg,
                    #A78BFA,
                    #8B5CF6,
                    #818CF8
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }


        .hero-description {
            max-width: 690px;

            color: #94A3B8;

            font-size: 16px;
            line-height: 1.75;

            margin-bottom: 26px;
        }


        .hero-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
        }


        .hero-pill {
            padding: 8px 12px;

            border-radius: 10px;

            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);

            color: #CBD5E1;

            font-size: 12px;
        }


        /* ---------- SCORE CARD ---------- */

        .score-card {
            padding: 30px 24px;

            border-radius: 24px;

            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,0.055),
                    rgba(255,255,255,0.02)
                );

            border: 1px solid rgba(255,255,255,0.08);

            text-align: center;

            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.03);
        }


        .score-label {
            color: #94A3B8;

            font-size: 11px;
            font-weight: 700;

            letter-spacing: 1.5px;

            margin-bottom: 12px;
        }


        .score-number {
            color: #F8FAFC;

            font-size: 64px;
            line-height: 1;

            font-weight: 850;
        }


        .score-small {
            color: #64748B;
            font-size: 21px;
            font-weight: 600;
        }


        .score-bar {
            height: 7px;

            margin: 20px 0 14px;

            border-radius: 999px;

            background: #1E293B;

            overflow: hidden;
        }


        .score-fill {
            width: 88%;
            height: 100%;

            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    #8B5CF6,
                    #6366F1
                );
        }


        .score-status {
            color: #A78BFA;

            font-size: 13px;
            font-weight: 650;
        }


        /* ---------- SECTION ---------- */

        .section-heading {
            margin-top: 54px;
            margin-bottom: 8px;

            color: #F8FAFC;

            font-size: 28px;
            font-weight: 800;

            letter-spacing: -0.7px;
        }


        .section-description {
            color: #64748B;

            font-size: 14px;

            margin-bottom: 25px;
        }


        /* ---------- FEATURE CARDS ---------- */

        .feature-card {
            min-height: 210px;

            padding: 25px;

            border-radius: 20px;

            background: #111827;

            border: 1px solid rgba(255,255,255,0.06);

            transition:
                transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease;
        }


        .feature-card:hover {
            transform: translateY(-5px);

            border-color:
                rgba(139,92,246,0.32);

            box-shadow:
                0 18px 45px rgba(0,0,0,0.25);
        }


        .feature-icon {
            width: 46px;
            height: 46px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 14px;

            background:
                linear-gradient(
                    145deg,
                    rgba(139,92,246,0.20),
                    rgba(99,102,241,0.08)
                );

            border:
                1px solid rgba(139,92,246,0.20);

            color: #C4B5FD;

            font-size: 20px;

            margin-bottom: 17px;
        }


        .feature-title {
            color: #F8FAFC;

            font-size: 17px;
            font-weight: 750;

            margin-bottom: 9px;
        }


        .feature-text {
            color: #94A3B8;

            font-size: 13px;

            line-height: 1.7;
        }


        /* ---------- PROCESS ---------- */

        .process-wrapper {
            position: relative;
        }


        .process-line {
            position: absolute;

            top: 27px;
            left: 11%;
            right: 11%;

            height: 1px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(139,92,246,0.35),
                    transparent
                );
        }


        .step-card {
            position: relative;
            z-index: 2;

            padding: 23px;

            min-height: 165px;

            border-radius: 18px;

            background: #111827;

            border: 1px solid rgba(255,255,255,0.06);

            transition:
                transform 0.25s ease,
                border-color 0.25s ease;
        }


        .step-card:hover {
            transform: translateY(-4px);

            border-color:
                rgba(139,92,246,0.30);
        }


        .step-number {
            width: 42px;
            height: 42px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background:
                linear-gradient(
                    145deg,
                    #8B5CF6,
                    #6366F1
                );

            color: white;

            font-size: 12px;
            font-weight: 800;

            margin-bottom: 17px;

            box-shadow:
                0 8px 22px rgba(99,102,241,0.22);
        }


        .step-title {
            color: #F8FAFC;

            font-size: 16px;
            font-weight: 750;

            margin-bottom: 7px;
        }


        .step-text {
            color: #94A3B8;

            font-size: 13px;

            line-height: 1.65;
        }


        /* ---------- CTA ---------- */

        .cta-box {
            margin-top: 52px;

            padding: 35px 38px;

            border-radius: 23px;

            background:
                radial-gradient(
                    circle at 85% 20%,
                    rgba(139,92,246,0.18),
                    transparent 30%
                ),
                linear-gradient(
                    120deg,
                    rgba(139,92,246,0.14),
                    rgba(99,102,241,0.06)
                );

            border:
                1px solid rgba(139,92,246,0.22);

            text-align: center;
        }


        .cta-title {
            color: #F8FAFC;

            font-size: 25px;
            font-weight: 800;

            margin-bottom: 8px;
        }


        .cta-text {
            color: #94A3B8;

            font-size: 14px;

            line-height: 1.7;
        }


        /* ---------- BUTTONS ---------- */

        div.stButton > button {
            border-radius: 12px !important;
            min-height: 46px !important;

            font-weight: 700 !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease !important;
        }


        div.stButton > button:hover {
            transform: translateY(-2px) !important;
        }


        /* PRIMARY */

        div.stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #8B5CF6,
                    #6366F1
                ) !important;

            color: #FFFFFF !important;

            border: 1px solid
                rgba(167,139,250,0.45) !important;

            box-shadow:
                0 10px 28px
                rgba(99,102,241,0.28) !important;
        }


        div.stButton > button[kind="primary"]:hover {
            background:
                linear-gradient(
                    135deg,
                    #9F67FF,
                    #7167FF
                ) !important;

            box-shadow:
                0 14px 34px
                rgba(99,102,241,0.38) !important;
        }


        /* SECONDARY */

        div.stButton > button:not([kind="primary"]) {
            background:
                rgba(255,255,255,0.035) !important;

            color: #CBD5E1 !important;

            border: 1px solid
                rgba(255,255,255,0.10) !important;
        }


        div.stButton > button:not([kind="primary"]):hover {
            border-color:
                rgba(139,92,246,0.40) !important;

            color: #F8FAFC !important;

            background:
                rgba(139,92,246,0.08) !important;
        }


        /* ---------- FOOTER ---------- */

        .home-footer {
            padding: 35px 0 12px;

            text-align: center;

            color: #475569;

            font-size: 12px;
        }


        /* ---------- RESPONSIVE ---------- */

        @media (max-width: 900px) {

            .hero-grid {
                grid-template-columns: 1fr;
            }

            .hero-title {
                font-size: 45px;
            }

            .process-line {
                display: none;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        '<div class="home-wrapper">'
        '<div class="hero-shell">'
        '<div class="hero-grid">'

        '<div>'

        '<div class="hero-eyebrow">'
        '✦ AI Resume Intelligence'
        '</div>'

        '<div class="hero-title">'
        'Turn your resume into '
        '<span class="hero-gradient">opportunity.</span>'
        '</div>'

        '<div class="hero-description">'
        'Understand how your resume matches a target job description '
        'with ATS scoring, intelligent skill matching and actionable '
        'resume insights.'
        '</div>'

        '<div class="hero-pills">'
        '<div class="hero-pill">◈ ATS Scoring</div>'
        '<div class="hero-pill">⌁ Semantic Matching</div>'
        '<div class="hero-pill">✦ AI Insights</div>'
        '<div class="hero-pill">✓ PDF Reports</div>'
        '</div>'

        '</div>'

        '<div class="score-card">'

        '<div class="score-label">'
        'SAMPLE ATS ANALYSIS'
        '</div>'

        '<div class="score-number">'
        '88<span class="score-small">/100</span>'
        '</div>'

        '<div class="score-bar">'
        '<div class="score-fill"></div>'
        '</div>'

        '<div class="score-status">'
        '● Strong Resume Alignment'
        '</div>'

        '</div>'

        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # HERO BUTTON — CENTER
    # ========================================================

    st.markdown(
        "<div style='height:16px'></div>",
        unsafe_allow_html=True,
    )

    hero_left, hero_center, hero_right = st.columns(
        [1, 1.25, 1]
    )

    with hero_center:

        if st.button(
            "🚀  Analyze My Resume",
            key="home_analyze_btn",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["current_page"] = "analyze"
            st.rerun()


    # ========================================================
    # FEATURES
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        'Intelligence behind your resume'
        '</div>'
        '<div class="section-description">'
        'More than a keyword checker — understand what your resume '
        'communicates to an ATS and a target role.'
        '</div>',
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(
        3,
        gap="large",
    )


    features = [
        (
            col1,
            "◉",
            "ATS Score",
            "Get a structured compatibility score based on required "
            "skills, preferred skills, relevance, structure and "
            "content completeness.",
        ),
        (
            col2,
            "⌁",
            "Hybrid Skill Matching",
            "Combine exact skill matching with semantic similarity "
            "to identify matched, related and missing skills from "
            "a target role.",
        ),
        (
            col3,
            "✦",
            "Actionable Insights",
            "Discover strengths, missing skills and practical "
            "recommendations without suggesting skills you do not "
            "actually have.",
        ),
    ]


    for column, icon, title, description in features:

        with column:

            st.markdown(
                f'<div class="feature-card">'
                f'<div class="feature-icon">{icon}</div>'
                f'<div class="feature-title">{title}</div>'
                f'<div class="feature-text">{description}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


    # ========================================================
    # HOW IT WORKS
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        'From resume to insight'
        '</div>'
        '<div class="section-description">'
        'A simple four-stage analysis pipeline.'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="process-wrapper">'
        '<div class="process-line"></div>',
        unsafe_allow_html=True,
    )


    step1, step2, step3, step4 = st.columns(
        4,
        gap="medium",
    )


    steps = [
        (
            step1,
            "01",
            "Upload",
            "Upload your resume in PDF or DOCX format.",
        ),
        (
            step2,
            "02",
            "Understand",
            "Extract sections, content and relevant skills.",
        ),
        (
            step3,
            "03",
            "Match",
            "Compare your resume against the target job description.",
        ),
        (
            step4,
            "04",
            "Improve",
            "Get an ATS score, feedback and recommendations.",
        ),
    ]


    for column, number, title, description in steps:

        with column:

            st.markdown(
                f'<div class="step-card">'
                f'<div class="step-number">{number}</div>'
                f'<div class="step-title">{title}</div>'
                f'<div class="step-text">{description}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # CTA
    # ========================================================

    st.markdown(
        '<div class="cta-box">'
        '<div class="cta-title">'
        'Ready to understand your resume?'
        '</div>'
        '<div class="cta-text">'
        'Compare your resume with a target job description and '
        'discover where you already match — and where you can improve.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # CTA BUTTONS — CENTER
    # ========================================================

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )


    cta_left, cta_btn1, cta_btn2, cta_right = st.columns(
        [1.2, 1.25, 1.25, 1.2]
    )


    with cta_btn1:

        if st.button(
            "🚀  Start Analysis",
            key="home_cta_btn",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["current_page"] = "analyze"
            st.rerun()


    with cta_btn2:

        if st.button(
            "📊  View History",
            key="home_history_btn",
            use_container_width=True,
        ):
            st.session_state["current_page"] = "history"
            st.rerun()


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        '<div class="home-footer">'
        'AI Resume ATS &nbsp;•&nbsp; FastAPI &nbsp;•&nbsp; '
        'Streamlit &nbsp;•&nbsp; NLP &nbsp;•&nbsp; Semantic AI'
        '</div>',
        unsafe_allow_html=True,
    )