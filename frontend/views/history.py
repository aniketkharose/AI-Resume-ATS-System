from datetime import datetime
from html import escape

import streamlit as st

from backend.database.supabase_db import get_user_analyses


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
        return "Strong"
    if score >= 60:
        return "Moderate"
    return "Needs Improvement"


def _format_date(created_at) -> str:
    if not created_at:
        return ""
    try:
        dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y • %I:%M %p")
    except Exception:
        return str(created_at)


def _css():
    st.markdown(
        """
        <style>
            .hs-title {
                font-size: 34px; font-weight: 800; color: #F8FAFC;
                letter-spacing: -0.8px; line-height: 1.1;
            }
            .hs-title span { color: #A78BFA; }
            .hs-subtitle { color: #94A3B8; font-size: 14.5px; margin: 8px 0 26px 0; }

            .hs-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
            .hs-stat {
                background: linear-gradient(145deg, rgba(17,24,39,0.98), rgba(15,23,42,0.98));
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 18px; padding: 20px;
                display: flex; align-items: center; gap: 16px;
            }
            .hs-stat:hover { border-color: rgba(139,92,246,0.35); }
            .hs-stat-icon {
                width: 48px; height: 48px; border-radius: 14px; font-size: 22px;
                display: flex; align-items: center; justify-content: center;
                background: rgba(139,92,246,0.12);
                border: 1px solid rgba(139,92,246,0.25);
            }
            .hs-stat-num { font-size: 28px; font-weight: 800; color: #F8FAFC; line-height: 1; }
            .hs-stat-lbl { font-size: 12px; color: #94A3B8; margin-top: 6px; }

            .hs-section { margin: 34px 0 16px 0; font-size: 22px; font-weight: 800; color: #F8FAFC; }
            .hs-section small { font-size: 13px; color: #64748B; font-weight: 500; margin-left: 8px; }

            .hs-empty {
                text-align: center; padding: 60px 20px; border-radius: 20px;
                background: rgba(255,255,255,0.02);
                border: 1.5px dashed rgba(139,92,246,0.35);
            }
            .hs-empty-icon { font-size: 46px; }
            .hs-empty-title { font-size: 20px; font-weight: 750; color: #F8FAFC; margin-top: 10px; }
            .hs-empty-text { color: #94A3B8; font-size: 14px; margin-top: 6px; }

            /* History card (keyed container) */
            [class*="st-key-hist_"] {
                background: linear-gradient(145deg, rgba(17,24,39,0.98), rgba(15,23,42,0.98));
                border: 1px solid rgba(255,255,255,0.07) !important;
                border-radius: 18px;
                padding: 20px;
                transition: all 0.2s ease;
            }
            [class*="st-key-hist_"]:hover {
                border-color: rgba(139,92,246,0.40) !important;
                box-shadow: 0 12px 32px rgba(0,0,0,0.25);
            }

            .hs-row { display: flex; align-items: center; gap: 22px; }
            .hs-ring {
                width: 84px; height: 84px; flex-shrink: 0; border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(255,255,255,0.08) 0);
            }
            .hs-ring-inner {
                width: 66px; height: 66px; border-radius: 50%; background: #0F1424;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
            }
            .hs-ring-num { font-size: 22px; font-weight: 800; color: #F8FAFC; line-height: 1; }
            .hs-ring-sub { font-size: 9px; color: #64748B; margin-top: 2px; }

            .hs-info { min-width: 0; flex: 1; }
            .hs-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
            .hs-file {
                font-size: 17px; font-weight: 750; color: #F1F5F9;
                overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%;
            }
            .hs-badge {
                display: inline-block; padding: 4px 10px; border-radius: 999px;
                font-size: 10.5px; font-weight: 800; letter-spacing: 0.8px;
                text-transform: uppercase;
            }
            .hs-date { color: #64748B; font-size: 12.5px; margin-top: 4px; }

            .hs-bar-wrap { margin-top: 14px; }
            .hs-bar-head {
                display: flex; justify-content: space-between;
                font-size: 12px; color: #94A3B8; margin-bottom: 6px;
            }
            .hs-bar {
                width: 100%; height: 7px; border-radius: 99px;
                background: rgba(255,255,255,0.08); overflow: hidden;
            }
            .hs-bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #8B5CF6, #6366F1); }

            .hs-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
            .hs-chip {
                padding: 4px 11px; border-radius: 999px; font-size: 12px; font-weight: 600;
                background: rgba(239,68,68,0.10); border: 1px solid rgba(239,68,68,0.30); color: #FCA5A5;
            }
            .hs-chip-more { background: rgba(148,163,184,0.12); border-color: rgba(148,163,184,0.25); color: #CBD5E1; }
            .hs-none { color: #6EE7B7; font-size: 12.5px; margin-top: 14px; }

            @media (max-width: 900px) {
                .hs-stats { grid-template-columns: 1fr; }
                .hs-row { flex-direction: column; align-items: flex-start; }
            }

            /* View button */
            [class*="st-key-view_"] button {
                height: 46px !important; border-radius: 12px !important; margin-top: 6px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN
# ============================================================

def render_history():
    """Render the user's resume analysis history."""

    _css()

    st.markdown(
        _h(
            """
            <div class="hs-title">Analysis <span>History</span></div>
            <div class="hs-subtitle">
                View your previous resume analyses and ATS results.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---------------- AUTH ----------------

    user = st.session_state.get("user")
    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")

    if not user:
        st.warning("Please log in to view your analysis history.")
        return

    if not access_token or not refresh_token:
        st.warning("Your authentication session is missing. Please log in again.")
        return

    # ---------------- FETCH ----------------

    try:
        history = get_user_analyses(
            user_id=str(user.id),
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except Exception as e:
        st.error(f"❌ Failed to load analysis history: {e}")
        return

    # ---------------- EMPTY STATE ----------------

    if not history:

        st.markdown(
            _h(
                """
                <div class="hs-empty">
                    <div class="hs-empty-icon">📄</div>
                    <div class="hs-empty-title">No analyses yet</div>
                    <div class="hs-empty-text">
                        Analyze your first resume to see it here.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        _, mid, _ = st.columns([1, 1, 1])
        with mid:
            if st.button(
                "🚀 Analyze Resume",
                type="primary",
                use_container_width=True,
                key="hist_empty_cta",
            ):
                st.session_state["current_page"] = "analyze"
                st.rerun()
        return

    # ---------------- STATS ----------------

    total = len(history)
    average_score = sum(_clamp(i.get("ats_score", 0)) for i in history) / total
    latest_score = _clamp(history[0].get("ats_score", 0))

    st.markdown(
        _h(
            f"""
            <div class="hs-stats">
                <div class="hs-stat">
                    <div class="hs-stat-icon">📚</div>
                    <div>
                        <div class="hs-stat-num">{total}</div>
                        <div class="hs-stat-lbl">Total Analyses</div>
                    </div>
                </div>
                <div class="hs-stat">
                    <div class="hs-stat-icon">📈</div>
                    <div>
                        <div class="hs-stat-num">{average_score:.1f}</div>
                        <div class="hs-stat-lbl">Average ATS Score</div>
                    </div>
                </div>
                <div class="hs-stat">
                    <div class="hs-stat-icon">🎯</div>
                    <div>
                        <div class="hs-stat-num">{latest_score:.1f}</div>
                        <div class="hs-stat-lbl">Latest ATS Score</div>
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="hs-section">📋 Previous Analyses<small>{total} total</small></div>',
        unsafe_allow_html=True,
    )

    # ---------------- CARDS ----------------

    for index, item in enumerate(history):

        item_id = item.get("id", index)

        filename = escape(str(item.get("filename", "Unknown Resume")))
        ats_score = _clamp(item.get("ats_score", 0))
        keyword_match = _clamp(item.get("keyword_match", 0))
        missing_keywords = item.get("missing_keywords", []) or []
        date_text = escape(_format_date(item.get("created_at", "")))

        color = _score_color(ats_score)
        label = _score_label(ats_score)

        if missing_keywords:
            chips = "".join(
                f'<span class="hs-chip">{escape(str(s))}</span>'
                for s in missing_keywords[:6]
            )
            extra = len(missing_keywords) - 6
            if extra > 0:
                chips += f'<span class="hs-chip hs-chip-more">+{extra} more</span>'
            missing_html = f'<div class="hs-chips">{chips}</div>'
        else:
            missing_html = '<div class="hs-none">✓ No missing skills recorded.</div>'

        with st.container(key=f"hist_{item_id}"):

            st.markdown(
                _h(
                    f"""
                    <div class="hs-row">
                        <div class="hs-ring" style="--p:{ats_score:.0f};--c:{color};">
                            <div class="hs-ring-inner">
                                <div class="hs-ring-num">{ats_score:.0f}</div>
                                <div class="hs-ring-sub">/ 100</div>
                            </div>
                        </div>
                        <div class="hs-info">
                            <div class="hs-top">
                                <div class="hs-file">📄 {filename}</div>
                                <span class="hs-badge"
                                      style="background:{color}22;color:{color};">{label}</span>
                            </div>
                            <div class="hs-date">Analyzed on {date_text}</div>
                            <div class="hs-bar-wrap">
                                <div class="hs-bar-head">
                                    <span>Keyword Match</span>
                                    <span>{keyword_match:.0f}%</span>
                                </div>
                                <div class="hs-bar">
                                    <div class="hs-bar-fill" style="width:{keyword_match:.0f}%;"></div>
                                </div>
                            </div>
                            {missing_html}
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

            if st.container(key=f"view_{item_id}").button(
                "View Full Analysis →",
                key=f"view_analysis_{item_id}",
                use_container_width=True,
            ):
                st.session_state["selected_history_analysis"] = item
                st.session_state["current_page"] = "analysis_detail"
                st.rerun()

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)