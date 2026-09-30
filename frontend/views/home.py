import re
from html import escape

import streamlit as st

from backend.database.supabase_db import get_user_analyses


# ============================================================
# HELPERS
# ============================================================

def _h(content: str) -> str:
    """Flatten HTML so Streamlit never treats it as a code block."""
    return "".join(line.strip() for line in content.splitlines())


def _display_name(user) -> str:
    email = getattr(user, "email", "") or ""
    name = email.split("@")[0]
    name = re.sub(r"[\d_.\-]+", " ", name).strip()
    return escape(name.title()) if name else "there"


def _load_activity(user):
    """Return (total, latest_score) or None."""
    try:
        history = get_user_analyses(
            user_id=str(user.id),
            access_token=st.session_state.get("access_token"),
            refresh_token=st.session_state.get("refresh_token"),
        )
        if not history:
            return 0, 0.0
        return len(history), float(history[0].get("ats_score", 0))
    except Exception:
        return None


def _css():
    st.markdown(
        """
        <style>

        .hm-wrap { max-width: 1180px; margin: 0 auto; }

        /* ---------- HERO ---------- */
        .hm-hero {
            padding: 52px 48px; border-radius: 30px;
            border: 1px solid rgba(139,92,246,0.25);
            background:
                radial-gradient(circle at 90% 10%, rgba(139,92,246,0.24), transparent 34%),
                radial-gradient(circle at 8% 92%, rgba(99,102,241,0.14), transparent 36%),
                #0F1422;
            box-shadow: 0 30px 80px rgba(0,0,0,0.35);
        }
        .hm-hero-grid {
            display: grid; grid-template-columns: 1.4fr 0.8fr;
            gap: 44px; align-items: center;
        }
        .hm-eyebrow {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 8px 14px; margin-bottom: 20px; border-radius: 999px;
            background: rgba(139,92,246,0.10); border: 1px solid rgba(139,92,246,0.28);
            color: #C4B5FD; font-size: 13px; font-weight: 650;
        }
        .hm-eyebrow i {
            width: 7px; height: 7px; border-radius: 50%; background: #A78BFA;
            box-shadow: 0 0 10px #A78BFA; display: inline-block;
        }
        .hm-title {
            color: #F8FAFC; font-size: 56px; line-height: 1.05;
            font-weight: 850; letter-spacing: -2.6px; margin-bottom: 22px;
        }
        .hm-grad {
            background: linear-gradient(90deg, #A78BFA, #8B5CF6, #818CF8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hm-desc {
            max-width: 620px; color: #94A3B8; font-size: 16px;
            line-height: 1.75; margin-bottom: 26px;
        }
        .hm-pills { display: flex; flex-wrap: wrap; gap: 9px; }
        .hm-pill {
            padding: 8px 13px; border-radius: 10px; font-size: 12.5px;
            background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08);
            color: #CBD5E1;
        }

        /* ---------- PREVIEW CARD ---------- */
        .hm-preview {
            padding: 26px 24px; border-radius: 24px;
            background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.09);
            box-shadow: 0 20px 50px rgba(0,0,0,0.30);
        }
        .hm-prev-label {
            color: #94A3B8; font-size: 11px; font-weight: 700;
            letter-spacing: 1.5px; text-align: center;
        }
        .hm-ring {
            width: 128px; height: 128px; border-radius: 50%; margin: 18px auto 14px;
            display: flex; align-items: center; justify-content: center;
            background: conic-gradient(#8B5CF6 88%, rgba(255,255,255,0.08) 0);
            box-shadow: 0 0 40px rgba(139,92,246,0.35);
        }
        .hm-ring-in {
            width: 100px; height: 100px; border-radius: 50%; background: #0F1424;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .hm-ring-num { font-size: 34px; font-weight: 850; color: #F8FAFC; line-height: 1; }
        .hm-ring-sub { font-size: 11px; color: #64748B; margin-top: 2px; }
        .hm-status {
            text-align: center; color: #6EE7B7; font-size: 13px; font-weight: 700; margin-bottom: 16px;
        }
        .hm-mini { margin-top: 10px; }
        .hm-mini-head {
            display: flex; justify-content: space-between;
            font-size: 11.5px; color: #94A3B8; margin-bottom: 5px;
        }
        .hm-mini-bar { height: 6px; border-radius: 99px; background: #1E293B; overflow: hidden; }
        .hm-mini-fill {
            height: 100%; border-radius: 99px;
            background: linear-gradient(90deg, #8B5CF6, #6366F1);
        }

        /* ---------- STATS STRIP ---------- */
        .hm-strip {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 22px;
        }
        .hm-strip-item {
            padding: 16px 18px; border-radius: 16px; text-align: center;
            background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
        }
        .hm-strip-num { font-size: 24px; font-weight: 850; color: #F8FAFC; }
        .hm-strip-lbl { font-size: 12px; color: #94A3B8; margin-top: 4px; }

        /* ---------- ACTIVITY ---------- */
        .hm-activity {
            display: flex; align-items: center; justify-content: space-between;
            gap: 18px; flex-wrap: wrap; margin-top: 22px;
            padding: 18px 24px; border-radius: 18px;
            background: linear-gradient(120deg, rgba(139,92,246,0.12), rgba(99,102,241,0.05));
            border: 1px solid rgba(139,92,246,0.25);
        }
        .hm-act-title { color: #F8FAFC; font-weight: 750; font-size: 15px; }
        .hm-act-sub { color: #94A3B8; font-size: 12.5px; margin-top: 3px; }
        .hm-act-stats { display: flex; gap: 26px; }
        .hm-act-num { color: #F8FAFC; font-size: 22px; font-weight: 850; line-height: 1; }
        .hm-act-lbl { color: #94A3B8; font-size: 11.5px; margin-top: 4px; }

        /* ---------- SECTIONS ---------- */
        .hm-heading {
            margin: 54px 0 8px; color: #F8FAFC; font-size: 28px;
            font-weight: 800; letter-spacing: -0.7px;
        }
        .hm-sub { color: #64748B; font-size: 14px; margin-bottom: 24px; }

        /* ---------- FEATURES ---------- */
        .hm-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
        .hm-feature {
            padding: 24px; border-radius: 20px;
            background: linear-gradient(145deg, rgba(17,24,39,0.98), rgba(15,23,42,0.98));
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.25s ease;
        }
        .hm-feature:hover {
            transform: translateY(-5px); border-color: rgba(139,92,246,0.35);
            box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        }
        .hm-icon {
            width: 48px; height: 48px; border-radius: 14px; font-size: 22px;
            display: flex; align-items: center; justify-content: center; margin-bottom: 16px;
            background: linear-gradient(145deg, rgba(139,92,246,0.22), rgba(99,102,241,0.08));
            border: 1px solid rgba(139,92,246,0.22);
        }
        .hm-f-title { color: #F8FAFC; font-size: 17px; font-weight: 750; margin-bottom: 8px; }
        .hm-f-text { color: #94A3B8; font-size: 13.5px; line-height: 1.7; }

        /* ---------- PROCESS ---------- */
        .hm-steps { position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
        .hm-steps::before {
            content: ""; position: absolute; top: 44px; left: 12%; right: 12%; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(139,92,246,0.45), transparent);
        }
        .hm-step {
            position: relative; padding: 22px; border-radius: 18px;
            background: #111827; border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.25s ease;
        }
        .hm-step:hover { transform: translateY(-4px); border-color: rgba(139,92,246,0.32); }
        .hm-num {
            width: 42px; height: 42px; border-radius: 50%; margin-bottom: 16px;
            display: flex; align-items: center; justify-content: center;
            background: linear-gradient(145deg, #8B5CF6, #6366F1);
            color: #FFFFFF; font-size: 13px; font-weight: 800;
            box-shadow: 0 8px 22px rgba(99,102,241,0.30);
        }

        /* ---------- CTA ---------- */
        .hm-cta {
            margin-top: 54px; padding: 36px 38px; border-radius: 24px; text-align: center;
            background:
                radial-gradient(circle at 85% 20%, rgba(139,92,246,0.20), transparent 32%),
                linear-gradient(120deg, rgba(139,92,246,0.14), rgba(99,102,241,0.06));
            border: 1px solid rgba(139,92,246,0.24);
        }
        .hm-cta-title { color: #F8FAFC; font-size: 26px; font-weight: 800; margin-bottom: 8px; }
        .hm-cta-text { color: #94A3B8; font-size: 14.5px; line-height: 1.7; }

        .hm-footer { padding: 36px 0 10px; text-align: center; color: #475569; font-size: 12px; }

        /* Home CTA buttons */
        [class*="st-key-home_"] button { height: 52px !important; border-radius: 14px !important; font-size: 15px !important; }

        @media (max-width: 900px) {
            .hm-hero { padding: 32px 24px; }
            .hm-hero-grid, .hm-grid-3, .hm-steps { grid-template-columns: 1fr; }
            .hm-strip { grid-template-columns: repeat(2, 1fr); }
            .hm-title { font-size: 40px; letter-spacing: -1.6px; }
            .hm-steps::before { display: none; }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home():

    _css()

    user = st.session_state.get("user")
    name = _display_name(user) if user else "there"

    # ========================================================
    # HERO
    # ========================================================

    breakdown = [
        ("Required Skills", 92),
        ("Semantic Relevance", 85),
        ("Resume Structure", 90),
    ]

    mini = "".join(
        _h(
            f"""
            <div class="hm-mini">
                <div class="hm-mini-head"><span>{label}</span><span>{value}%</span></div>
                <div class="hm-mini-bar"><div class="hm-mini-fill" style="width:{value}%;"></div></div>
            </div>
            """
        )
        for label, value in breakdown
    )

    st.markdown(
        _h(
            f"""
            <div class="hm-wrap">
            <div class="hm-hero">
            <div class="hm-hero-grid">

                <div>
                    <div class="hm-eyebrow"><i></i>Welcome back, {name}</div>
                    <div class="hm-title">Turn your resume into <span class="hm-grad">opportunity.</span></div>
                    <div class="hm-desc">Understand how your resume matches a target job description with ATS scoring, intelligent skill matching and actionable resume insights.</div>
                    <div class="hm-pills">
                        <div class="hm-pill">🎯 ATS Scoring</div>
                        <div class="hm-pill">🧠 Semantic Matching</div>
                        <div class="hm-pill">✨ AI Insights</div>
                        <div class="hm-pill">📄 PDF Reports</div>
                    </div>
                </div>

                <div class="hm-preview">
                    <div class="hm-prev-label">SAMPLE ATS ANALYSIS</div>
                    <div class="hm-ring">
                        <div class="hm-ring-in">
                            <div class="hm-ring-num">88</div>
                            <div class="hm-ring-sub">/ 100</div>
                        </div>
                    </div>
                    <div class="hm-status">● Strong Resume Alignment</div>
                    {mini}
                </div>

            </div>
            </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ========================================================
    # HERO BUTTONS
    # ========================================================

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    _, b1, b2, _ = st.columns([0.6, 1.2, 1.2, 0.6], gap="medium")

    with b1:
        if st.button(
            "🚀  Analyze My Resume",
            key="home_analyze_btn",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["current_page"] = "analyze"
            st.rerun()

    with b2:
        if st.button(
            "📊  View History",
            key="home_history_top",
            use_container_width=True,
        ):
            st.session_state["current_page"] = "history"
            st.rerun()

    # ========================================================
    # STATS STRIP
    # ========================================================

    st.markdown(
        _h(
            """
            <div class="hm-strip">
                <div class="hm-strip-item"><div class="hm-strip-num">5</div><div class="hm-strip-lbl">Scoring dimensions</div></div>
                <div class="hm-strip-item"><div class="hm-strip-num">Hybrid</div><div class="hm-strip-lbl">Exact + semantic match</div></div>
                <div class="hm-strip-item"><div class="hm-strip-num">PDF · DOCX</div><div class="hm-strip-lbl">Supported formats</div></div>
                <div class="hm-strip-item"><div class="hm-strip-num">PDF</div><div class="hm-strip-lbl">Downloadable report</div></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ========================================================
    # ACTIVITY (only if data available)
    # ========================================================

    activity = _load_activity(user) if user else None

    if activity is not None:
        total, latest = activity

        if total == 0:
            st.markdown(
                _h(
                    """
                    <div class="hm-activity">
                        <div>
                            <div class="hm-act-title">You have not analyzed a resume yet</div>
                            <div class="hm-act-sub">Upload your first resume to see your ATS score.</div>
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                _h(
                    f"""
                    <div class="hm-activity">
                        <div>
                            <div class="hm-act-title">Your activity</div>
                            <div class="hm-act-sub">Pick up where you left off.</div>
                        </div>
                        <div class="hm-act-stats">
                            <div><div class="hm-act-num">{total}</div><div class="hm-act-lbl">Analyses</div></div>
                            <div><div class="hm-act-num">{latest:.0f}</div><div class="hm-act-lbl">Latest ATS score</div></div>
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

    # ========================================================
    # FEATURES
    # ========================================================

    features = [
        ("🎯", "ATS Score", "Get a structured compatibility score based on required skills, preferred skills, relevance, structure and content completeness."),
        ("🧠", "Hybrid Skill Matching", "Combine exact skill matching with semantic similarity to identify matched, related and missing skills from a target role."),
        ("💡", "Actionable Insights", "Discover strengths, missing skills and practical recommendations without suggesting skills you do not actually have."),
        ("📊", "Score Breakdown", "See exactly which dimension pulls your score up or down, with a clear percentage for each one."),
        ("🗂️", "Saved History", "Every analysis is saved to your account, so you can revisit results and track your progress over time."),
        ("📄", "PDF Report", "Generate a complete ATS report as a PDF that you can download and keep."),
    ]

    cards = "".join(
        _h(
            f"""
            <div class="hm-feature">
                <div class="hm-icon">{icon}</div>
                <div class="hm-f-title">{title}</div>
                <div class="hm-f-text">{text}</div>
            </div>
            """
        )
        for icon, title, text in features
    )

    st.markdown(
        _h(
            """
            <div class="hm-heading">Intelligence behind your resume</div>
            <div class="hm-sub">More than a keyword checker. Understand what your resume communicates to an ATS and a target role.</div>
            """
        )
        + f'<div class="hm-grid-3">{cards}</div>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # HOW IT WORKS
    # ========================================================

    steps = [
        ("01", "Upload", "Upload your resume in PDF or DOCX format."),
        ("02", "Understand", "Extract sections, content and relevant skills."),
        ("03", "Match", "Compare your resume against the target job description."),
        ("04", "Improve", "Get an ATS score, feedback and recommendations."),
    ]

    step_cards = "".join(
        _h(
            f"""
            <div class="hm-step">
                <div class="hm-num">{num}</div>
                <div class="hm-f-title">{title}</div>
                <div class="hm-f-text">{text}</div>
            </div>
            """
        )
        for num, title, text in steps
    )

    st.markdown(
        _h(
            """
            <div class="hm-heading">From resume to insight</div>
            <div class="hm-sub">A simple four-stage analysis pipeline.</div>
            """
        )
        + f'<div class="hm-steps">{step_cards}</div>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # CTA
    # ========================================================

    st.markdown(
        _h(
            """
            <div class="hm-cta">
                <div class="hm-cta-title">Ready to understand your resume?</div>
                <div class="hm-cta-text">Compare your resume with a target job description and discover where you already match, and where you can improve.</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    _, c1, c2, _ = st.columns([0.6, 1.2, 1.2, 0.6], gap="medium")

    with c1:
        if st.button(
            "🚀  Start Analysis",
            key="home_cta_btn",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["current_page"] = "analyze"
            st.rerun()

    with c2:
        if st.button(
            "👤  My Profile",
            key="home_profile_btn",
            use_container_width=True,
        ):
            st.session_state["current_page"] = "profile"
            st.rerun()

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        '<div class="hm-footer">AI Resume ATS &nbsp;•&nbsp; FastAPI &nbsp;•&nbsp; Streamlit &nbsp;•&nbsp; NLP &nbsp;•&nbsp; Semantic AI</div>',
        unsafe_allow_html=True,
    )