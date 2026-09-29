import os
import tempfile
from html import escape

import streamlit as st

from backend.services.report_generator import generate_ats_report


# ============================================================
# HELPERS
# ============================================================

def _h(content: str) -> str:
    """Flatten HTML so Streamlit never treats it as a code block."""
    return "".join(line.strip() for line in content.splitlines())


def _clamp(value, low=0.0, high=100.0) -> float:
    try:
        return max(low, min(high, float(value)))
    except (TypeError, ValueError):
        return low


def _score_color(score: float) -> str:
    if score >= 80:
        return "#10B981"
    if score >= 60:
        return "#F59E0B"
    return "#EF4444"


def _score_label(score: float) -> str:
    if score >= 80:
        return "Strong ATS compatibility"
    if score >= 60:
        return "Moderate ATS compatibility"
    return "Resume needs improvement"


def _bar(pct: float, color: str = "#8B5CF6") -> str:
    pct = _clamp(pct)
    return _h(
        f"""
        <div class="ad-bar">
            <div class="ad-bar-fill" style="width:{pct:.0f}%;background:{color};"></div>
        </div>
        """
    )


def _section(icon: str, title: str, subtitle: str = ""):
    sub = f'<div class="ad-section-sub">{escape(subtitle)}</div>' if subtitle else ""
    st.markdown(
        _h(
            f"""
            <div class="ad-section">
                <div class="ad-section-title"><span>{icon}</span>{escape(title)}</div>
                {sub}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _sub(title: str):
    st.markdown(
        f'<div class="ad-sub">{title}</div>',
        unsafe_allow_html=True,
    )


def _feedback_items(items, default_title):
    """Normalize feedback items (dict or str) to (title, description)."""
    out = []
    for item in items or []:
        if isinstance(item, dict):
            title = item.get("title") or item.get("message") or default_title
            desc = item.get("description", "")
            out.append((str(title), str(desc) if desc else ""))
        else:
            out.append((str(item), ""))
    return out


def _css():
    st.markdown(
        """
        <style>
            .ad-title {
                font-size: 34px; font-weight: 800; color: #F8FAFC;
                letter-spacing: -0.8px; line-height: 1.1;
            }
            .ad-title span { color: #A78BFA; }
            .ad-file {
                display: inline-flex; align-items: center; gap: 8px;
                margin: 10px 0 22px 0; padding: 6px 14px; border-radius: 999px;
                background: rgba(139,92,246,0.10);
                border: 1px solid rgba(139,92,246,0.30);
                color: #C4B5FD; font-size: 13px; font-weight: 600;
            }

            .ad-section { margin: 34px 0 16px 0; }
            .ad-section-title {
                font-size: 22px; font-weight: 800; color: #F8FAFC;
                display: flex; align-items: center; gap: 10px;
            }
            .ad-section-sub { color: #64748B; font-size: 13.5px; margin-top: 4px; }
            .ad-sub {
                font-size: 15px; font-weight: 700; color: #CBD5E1;
                margin: 22px 0 12px 0;
            }

            .ad-card {
                background: linear-gradient(145deg, rgba(17,24,39,0.98), rgba(15,23,42,0.98));
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 18px; padding: 20px;
                height: 100%; box-sizing: border-box;
            }
            .ad-card:hover { border-color: rgba(139,92,246,0.35); }
            .ad-label {
                font-size: 11px; font-weight: 700; letter-spacing: 1.3px;
                color: #64748B; text-transform: uppercase;
            }

            /* Score ring */
            .ad-hero { display: flex; align-items: center; gap: 24px; }
            .ad-ring {
                width: 150px; height: 150px; flex-shrink: 0; border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(255,255,255,0.08) 0);
                box-shadow: 0 0 40px color-mix(in srgb, var(--c) 30%, transparent);
            }
            .ad-ring-inner {
                width: 118px; height: 118px; border-radius: 50%;
                background: #0F1424;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
            }
            .ad-ring-num { font-size: 40px; font-weight: 800; color: #F8FAFC; line-height: 1; }
            .ad-ring-sub { font-size: 12px; color: #64748B; margin-top: 2px; }
            .ad-verdict { font-size: 17px; font-weight: 700; margin-top: 8px; }

            .ad-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px; }
            .ad-stat {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px; padding: 14px;
            }
            .ad-stat-num { font-size: 28px; font-weight: 800; color: #F8FAFC; }
            .ad-stat-lbl { font-size: 12px; color: #94A3B8; margin-top: 2px; }

            .ad-bar {
                width: 100%; height: 8px; border-radius: 99px;
                background: rgba(255,255,255,0.08); overflow: hidden; margin-top: 12px;
            }
            .ad-bar-fill { height: 100%; border-radius: 99px; }

            /* Grids */
            .ad-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
            .ad-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
            @media (max-width: 900px) {
                .ad-grid-3, .ad-grid-2 { grid-template-columns: 1fr; }
                .ad-hero { flex-direction: column; text-align: center; }
            }

            /* Breakdown */
            .ad-bd-icon { font-size: 26px; }
            .ad-bd-name { font-weight: 700; color: #F8FAFC; margin-top: 8px; }
            .ad-bd-score { font-size: 32px; font-weight: 800; margin: 4px 0; }
            .ad-bd-desc { font-size: 12.5px; color: #64748B; }

            /* Chips & badges */
            .ad-chips { display: flex; flex-wrap: wrap; gap: 10px; }
            .ad-chip {
                display: inline-flex; align-items: center; gap: 8px;
                padding: 8px 14px; border-radius: 999px;
                font-size: 13.5px; font-weight: 600;
            }
            .ad-chip small { font-size: 10px; font-weight: 700; letter-spacing: 0.6px; opacity: 0.75; }
            .ad-chip-green { background: rgba(16,185,129,0.10); border: 1px solid rgba(16,185,129,0.35); color: #6EE7B7; }
            .ad-chip-red { background: rgba(239,68,68,0.10); border: 1px solid rgba(239,68,68,0.35); color: #FCA5A5; }

            .ad-badge {
                display: inline-block; padding: 4px 10px; border-radius: 999px;
                font-size: 10.5px; font-weight: 800; letter-spacing: 0.8px;
            }
            .ad-badge-red { background: rgba(239,68,68,0.15); color: #FCA5A5; }
            .ad-badge-amber { background: rgba(245,158,11,0.15); color: #FCD34D; }
            .ad-badge-blue { background: rgba(99,102,241,0.18); color: #A5B4FC; }
            .ad-badge-gray { background: rgba(148,163,184,0.15); color: #CBD5E1; }

            .ad-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; }
            .ad-item-title { font-weight: 700; color: #F1F5F9; font-size: 15px; }
            .ad-item-desc { color: #94A3B8; font-size: 13.5px; line-height: 1.6; margin-top: 6px; }
            .ad-item-meta { color: #64748B; font-size: 12px; margin-top: 8px; }

            .ad-summary { color: #CBD5E1; font-size: 15px; line-height: 1.75; }

            .ad-green-edge { border-left: 3px solid #10B981; }
            .ad-amber-edge { border-left: 3px solid #F59E0B; }
            .ad-red-edge { border-left: 3px solid #EF4444; }
            .ad-purple-edge { border-left: 3px solid #8B5CF6; }

            .ad-stack { display: flex; flex-direction: column; gap: 12px; }
            .ad-empty {
                padding: 16px; border-radius: 14px; color: #94A3B8; font-size: 14px;
                background: rgba(255,255,255,0.03); border: 1px dashed rgba(255,255,255,0.12);
            }
            .ad-success {
                padding: 16px; border-radius: 14px; color: #6EE7B7; font-size: 14px; font-weight: 600;
                background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.30);
            }

            /* Back button */
            .st-key-back_history button {
                min-height: 40px !important; border-radius: 999px !important;
                padding: 0 18px !important;
            }
            /* Report buttons */
            .st-key-gen_report button,
            .st-key-dl_report button {
                height: 52px !important;
                border-radius: 14px !important;
                font-size: 15px !important;
            }

            /* Download button (Streamlit ise alag testid se banata hai) */
            .st-key-dl_report button,
            [data-testid="stDownloadButton"] button {
                background: linear-gradient(135deg, #10B981, #059669) !important;
                border: 1px solid rgba(16,185,129,0.5) !important;
                box-shadow: 0 8px 24px rgba(16,185,129,0.25) !important;
            }

            .st-key-dl_report button *,
            [data-testid="stDownloadButton"] button * {
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            [data-testid="stDownloadButton"] button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 12px 30px rgba(16,185,129,0.40) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _empty(text: str) -> str:
    return f'<div class="ad-empty">{escape(text)}</div>'


# ============================================================
# MAIN
# ============================================================

def render_analysis_detail():
    """Render a complete saved resume analysis."""

    _css()

    # ---------------- GET SELECTED ANALYSIS ----------------

    analysis = st.session_state.get("selected_history_analysis")

    if not analysis:

        st.warning("No analysis selected.")

        if st.button("← Back to History", key="back_history_empty"):
            st.session_state["current_page"] = "history"
            st.rerun()

        return

    # ---------------- EXTRACT DATA ----------------

    filename = analysis.get("filename", "Resume")
    ats_score = _clamp(analysis.get("ats_score", 0))
    keyword_match = _clamp(analysis.get("keyword_match", 0))
    missing_keywords = analysis.get("missing_keywords", []) or []

    result = analysis.get("analysis_result", {}) or {}
    ats_data = result.get("ats", {}) or {}
    components = ats_data.get("components", {}) or {}
    matching_data = result.get("matching", {}) or {}
    feedback_data = result.get("feedback", {}) or {}
    recommendation_data = result.get("recommendations", {}) or {}

    # ---------------- HEADER ----------------

    if st.button("← Back to History", key="back_history"):
        st.session_state["current_page"] = "history"
        st.rerun()

    st.markdown(
        _h(
            f"""
            <div style="margin-top:14px;">
                <div class="ad-title">Analysis <span>Details</span></div>
                <div class="ad-file">📄 {escape(str(filename))}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ========================================================
    # ATS SCORE
    # ========================================================

    color = _score_color(ats_score)

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown(
            _h(
                f"""
                <div class="ad-card">
                    <div class="ad-label">Overall ATS Score</div>
                    <div class="ad-hero" style="margin-top:16px;">
                        <div class="ad-ring" style="--p:{ats_score:.0f};--c:{color};">
                            <div class="ad-ring-inner">
                                <div class="ad-ring-num">{ats_score:.0f}</div>
                                <div class="ad-ring-sub">/ 100</div>
                            </div>
                        </div>
                        <div>
                            <div class="ad-verdict" style="color:{color};">{_score_label(ats_score)}</div>
                            <div class="ad-item-desc">How well your resume matches the target job description.</div>
                        </div>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            _h(
                f"""
                <div class="ad-card">
                    <div class="ad-label">Score Overview</div>
                    <div class="ad-item-desc">{ats_score:.0f}% ATS compatibility</div>
                    {_bar(ats_score, color)}
                    <div class="ad-stats">
                        <div class="ad-stat">
                            <div class="ad-stat-num">{keyword_match:.0f}%</div>
                            <div class="ad-stat-lbl">Keyword Match</div>
                        </div>
                        <div class="ad-stat">
                            <div class="ad-stat-num">{len(missing_keywords)}</div>
                            <div class="ad-stat-lbl">Missing Skills</div>
                        </div>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    # ========================================================
    # BREAKDOWN
    # ========================================================

    _section(
        "📊",
        "ATS Score Breakdown",
        "See how your resume performed across each ATS dimension.",
    )

    breakdown = [
        ("🎯", "Required Skills", components.get("required_skills", 0),
         "Core skills requested by the job."),
        ("⭐", "Preferred Skills", components.get("preferred_skills", 0),
         "Additional skills marked as preferred."),
        ("🧠", "Semantic Relevance", components.get("semantic_relevance", 0),
         "Meaning-level similarity with the job."),
        ("📄", "Resume Structure", components.get("resume_structure", 0),
         "Presence of important resume sections."),
        ("📝", "Content Completeness", components.get("content_completeness", 0),
         "Overall resume content coverage."),
    ]

    cards = ""
    for icon, title, score, desc in breakdown:
        score = _clamp(score)
        c = _score_color(score)
        cards += _h(
            f"""
            <div class="ad-card">
                <div class="ad-bd-icon">{icon}</div>
                <div class="ad-bd-name">{escape(title)}</div>
                <div class="ad-bd-score" style="color:{c};">{score:.0f}%</div>
                <div class="ad-bd-desc">{escape(desc)}</div>
                {_bar(score, c)}
            </div>
            """
        )

    st.markdown(f'<div class="ad-grid-3">{cards}</div>', unsafe_allow_html=True)

    # ========================================================
    # SKILL MATCHING
    # ========================================================

    _section(
        "🎯",
        "Skill Matching",
        "Understand which job skills are present, related, or missing.",
    )

    matched_skills = matching_data.get("matched", []) or []
    related_skills = matching_data.get("related", []) or []
    missing_skills = matching_data.get("missing", []) or []

    # ---------------- Matched ----------------

    _sub("🟢 Matched Skills")

    if matched_skills:
        chips = ""
        for skill in matched_skills:
            name = escape(str(skill.get("jd_skill", "Unknown")))
            importance = str(skill.get("importance", "general")).upper()
            match_type = str(skill.get("match_type", "exact")).upper()
            chips += (
                f'<span class="ad-chip ad-chip-green">✓ {name}'
                f"<small>{escape(importance)} · {escape(match_type)}</small></span>"
            )
        st.markdown(f'<div class="ad-chips">{chips}</div>', unsafe_allow_html=True)
    else:
        st.markdown(_empty("No matched skills found."), unsafe_allow_html=True)

    # ---------------- Related ----------------

    if related_skills:
        _sub("🟡 Related Skills")

        cards = ""
        for skill in related_skills:
            jd_skill = escape(str(skill.get("jd_skill", "Unknown")))
            resume_skill = escape(str(skill.get("resume_skill", "Unknown")))
            similarity = _clamp(skill.get("similarity", 0), 0.0, 1.0)
            cards += _h(
                f"""
                <div class="ad-card ad-amber-edge">
                    <div class="ad-item-title">{jd_skill}</div>
                    <div class="ad-item-meta">Resume skill: {resume_skill}</div>
                    {_bar(similarity * 100, "#F59E0B")}
                    <div class="ad-item-meta">{similarity * 100:.1f}% semantic similarity</div>
                </div>
                """
            )

        st.markdown(f'<div class="ad-grid-2">{cards}</div>', unsafe_allow_html=True)

    # ---------------- Missing ----------------

    _sub("🔴 Missing Skills")

    if missing_skills:
        cards = ""
        for skill in missing_skills:
            name = escape(str(skill.get("jd_skill", "Unknown")))
            category = escape(str(skill.get("category", "General")))
            importance = str(skill.get("importance", "general")).lower()

            if importance == "required":
                badge = '<span class="ad-badge ad-badge-red">REQUIRED</span>'
            elif importance == "preferred":
                badge = '<span class="ad-badge ad-badge-amber">PREFERRED</span>'
            else:
                badge = '<span class="ad-badge ad-badge-gray">GENERAL</span>'

            cards += _h(
                f"""
                <div class="ad-card ad-red-edge">
                    <div class="ad-row">
                        <div>
                            <div class="ad-item-title">{name}</div>
                            <div class="ad-item-meta">{category}</div>
                        </div>
                        {badge}
                    </div>
                </div>
                """
            )

        st.markdown(f'<div class="ad-grid-2">{cards}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="ad-success">🎉 No missing skills detected!</div>',
            unsafe_allow_html=True,
        )

    # ========================================================
    # FEEDBACK
    # ========================================================

    _section(
        "💡",
        "Resume Feedback",
        "Understand what is working well and what can be improved.",
    )

    summary = feedback_data.get("summary", "No summary available.")

    st.markdown(
        _h(
            f"""
            <div class="ad-card ad-purple-edge">
                <div class="ad-label">Overall Summary</div>
                <div class="ad-summary" style="margin-top:10px;">{escape(str(summary))}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    strengths = _feedback_items(feedback_data.get("strengths", []), "Strength")
    improvements = _feedback_items(feedback_data.get("improvements", []), "Improvement")

    def _feedback_cards(items, edge, empty_text):
        if not items:
            return _empty(empty_text)
        out = ""
        for title, desc in items:
            d = f'<div class="ad-item-desc">{escape(desc)}</div>' if desc else ""
            out += _h(
                f"""
                <div class="ad-card {edge}">
                    <div class="ad-item-title">{escape(title)}</div>
                    {d}
                </div>
                """
            )
        return f'<div class="ad-stack">{out}</div>'

    col_s, col_i = st.columns(2, gap="large")

    with col_s:
        _sub("🟢 Strengths")
        st.markdown(
            _feedback_cards(strengths, "ad-green-edge", "No specific strengths identified."),
            unsafe_allow_html=True,
        )

    with col_i:
        _sub("⚠️ Improvements")
        st.markdown(
            _feedback_cards(improvements, "ad-amber-edge", "No specific improvements identified."),
            unsafe_allow_html=True,
        )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    _section(
        "🚀",
        "Recommendations",
        "Actionable suggestions based on this analysis.",
    )

    all_recommendations = []
    seen = set()

    def _add_rec(kind, item):
        # Sirf meaningful items lo, plain numbers/counts skip karo
        if isinstance(item, dict):
            key = (
                str(item.get("skill") or item.get("title") or "").lower(),
                str(
                    item.get("message")
                    or item.get("recommendation")
                    or item.get("description")
                    or ""
                ).lower(),
            )
        elif isinstance(item, str) and item.strip():
            key = ("", item.strip().lower())
        else:
            return  # int, float, bool, None skip

        if key in seen:
            return  # duplicate skip

        seen.add(key)
        all_recommendations.append((kind, item))

    if isinstance(recommendation_data, dict):
        for key, items in recommendation_data.items():
            if isinstance(items, list):
                for item in items:
                    _add_rec(key, item)
            elif isinstance(items, (dict, str)) and items:
                _add_rec(key, items)
            # numbers like "total": 1 ignore ho jayenge

    elif isinstance(recommendation_data, list):
        for item in recommendation_data:
            _add_rec("recommendation", item)
    if all_recommendations:
        cards = ""

        for index, (rec_type, rec_data) in enumerate(all_recommendations, start=1):

            if isinstance(rec_data, dict):
                title = rec_data.get(
                    "skill",
                    rec_data.get("title", f"Recommendation {index}"),
                )
                message = rec_data.get(
                    "message",
                    rec_data.get(
                        "recommendation",
                        rec_data.get("description", ""),
                    ),
                )
                priority = str(rec_data.get("priority", "")).upper()
            else:
                title = f"Recommendation {index}"
                message = str(rec_data)
                priority = ""

            if priority == "HIGH":
                badge = '<span class="ad-badge ad-badge-red">HIGH</span>'
            elif priority == "MEDIUM":
                badge = '<span class="ad-badge ad-badge-amber">MEDIUM</span>'
            elif priority:
                badge = f'<span class="ad-badge ad-badge-blue">{escape(priority)}</span>'
            else:
                badge = ""

            msg = f'<div class="ad-item-desc">{escape(str(message))}</div>' if message else ""
            kind = escape(str(rec_type).replace("_", " ").title())

            cards += _h(
                f"""
                <div class="ad-card ad-purple-edge">
                    <div class="ad-row">
                        <div class="ad-item-title">{escape(str(title))}</div>
                        {badge}
                    </div>
                    {msg}
                    <div class="ad-item-meta">{kind}</div>
                </div>
                """
            )

        st.markdown(f'<div class="ad-grid-2">{cards}</div>', unsafe_allow_html=True)

    else:
        st.markdown(
            _empty("No additional recommendations generated."),
            unsafe_allow_html=True,
        )

    # ========================================================
    # PDF REPORT
    # ========================================================

    _section(
        "📄",
        "ATS Report",
        "Download the complete ATS analysis as a PDF.",
    )

    report_key = f"ats_report_pdf::{filename}"

    _, mid, _ = st.columns([1, 2, 1])

    with mid:

        if st.button(
            "📄 Generate ATS Report",
            use_container_width=True,
            type="primary",
            key="gen_report",
        ):

            with st.spinner("Generating your ATS report..."):

                report_path = None

                try:

                    with tempfile.NamedTemporaryFile(
                        suffix=".pdf",
                        delete=False,
                    ) as temp_file:
                        report_path = temp_file.name

                    generate_ats_report(
                        output_path=report_path,
                        ats_result=result.get("ats", {}),
                        feedback=result.get("feedback", {}),
                        recommendations=result.get("recommendations", {}),
                        filename=filename,
                    )

                    with open(report_path, "rb") as pdf_file:
                        st.session_state[report_key] = pdf_file.read()

                except Exception as e:

                    st.session_state.pop(report_key, None)
                    st.error(f"❌ Failed to generate report: {e}")

                finally:

                    if report_path and os.path.exists(report_path):
                        os.remove(report_path)

        if st.session_state.get(report_key):

            st.markdown(
                '<div class="ad-success" style="margin:12px 0;">'
                "✅ ATS report generated successfully!</div>",
                unsafe_allow_html=True,
            )

            st.download_button(
                label="📥 Download ATS Report",
                data=st.session_state[report_key],
                file_name="ATS_Resume_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dl_report",
            )