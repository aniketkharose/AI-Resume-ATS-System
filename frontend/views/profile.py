from datetime import datetime
from html import escape

import streamlit as st

from backend.database.supabase_db import get_user_analyses


def _h(content: str) -> str:
    """Flatten HTML so Streamlit never treats it as a code block."""
    return "".join(line.strip() for line in content.splitlines())


def _member_since(user) -> str:
    created = getattr(user, "created_at", None)
    if not created:
        return "—"
    try:
        if isinstance(created, datetime):
            return created.strftime("%d %b %Y")
        dt = datetime.fromisoformat(str(created).replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y")
    except Exception:
        return str(created)


def _css():
    st.markdown(
        """
        <style>
            .pf-title {
                font-size: 34px; font-weight: 800; color: #F8FAFC;
                letter-spacing: -0.8px; line-height: 1.1;
            }
            .pf-title span { color: #A78BFA; }
            .pf-subtitle { color: #94A3B8; font-size: 14.5px; margin: 8px 0 26px 0; }

            .pf-card {
                background: linear-gradient(145deg, rgba(17,24,39,0.98), rgba(15,23,42,0.98));
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 20px; padding: 24px;
                height: 100%; box-sizing: border-box;
            }
            .pf-card:hover { border-color: rgba(139,92,246,0.35); }
            .pf-label {
                font-size: 11px; font-weight: 700; letter-spacing: 1.3px;
                color: #64748B; text-transform: uppercase;
            }

            .pf-head { display: flex; align-items: center; gap: 18px; margin-top: 16px; }
            .pf-avatar {
                width: 72px; height: 72px; border-radius: 50%; flex-shrink: 0;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px; font-weight: 800; color: #FFFFFF;
                background: linear-gradient(135deg, #8B5CF6, #6366F1);
                box-shadow: 0 10px 28px rgba(99,102,241,0.40);
            }
            .pf-email {
                font-size: 18px; font-weight: 750; color: #F8FAFC;
                overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
            }
            .pf-role { color: #94A3B8; font-size: 13px; margin-top: 4px; }

            .pf-field { margin-top: 18px; }
            .pf-field-lbl { font-size: 12px; color: #64748B; margin-bottom: 6px; }
            .pf-field-val {
                padding: 10px 14px; border-radius: 12px;
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.07);
                color: #E2E8F0; font-size: 13.5px;
                font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
                word-break: break-all;
            }

            .pf-status {
                display: inline-flex; align-items: center; gap: 8px; margin-top: 16px;
                padding: 8px 14px; border-radius: 999px;
                background: rgba(16,185,129,0.10); border: 1px solid rgba(16,185,129,0.35);
                color: #6EE7B7; font-size: 13px; font-weight: 700;
            }
            .pf-dot {
                width: 8px; height: 8px; border-radius: 50%; background: #10B981;
                box-shadow: 0 0 10px #10B981;
            }
            .pf-text { color: #94A3B8; font-size: 13.5px; line-height: 1.7; margin-top: 14px; }

            .pf-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 16px; }
            .pf-stat {
                background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px; padding: 14px;
            }
            .pf-stat-num { font-size: 24px; font-weight: 800; color: #F8FAFC; line-height: 1; }
            .pf-stat-lbl { font-size: 11.5px; color: #94A3B8; margin-top: 6px; }

            .pf-danger {
                margin-top: 30px; padding: 22px; border-radius: 20px;
                background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.25);
            }
            .pf-danger-title { font-size: 18px; font-weight: 750; color: #FCA5A5; }

            @media (max-width: 900px) { .pf-stats { grid-template-columns: 1fr; } }

            /* Logout button */
            .st-key-profile_logout button {
                height: 50px !important; border-radius: 14px !important;
                background: rgba(239,68,68,0.12) !important;
                border: 1px solid rgba(239,68,68,0.45) !important;
                box-shadow: none !important;
            }
            .st-key-profile_logout button * { color: #FCA5A5 !important; font-weight: 700 !important; }
            .st-key-profile_logout button:hover { background: rgba(239,68,68,0.22) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _load_stats(user):
    """Return (total, average, latest) or None if unavailable."""
    try:
        history = get_user_analyses(
            user_id=str(user.id),
            access_token=st.session_state.get("access_token"),
            refresh_token=st.session_state.get("refresh_token"),
        )
        if not history:
            return 0, 0.0, 0.0
        scores = [float(i.get("ats_score", 0)) for i in history]
        return len(scores), sum(scores) / len(scores), scores[0]
    except Exception:
        return None


def render_profile():

    user = st.session_state.get("user")

    if not user:
        st.warning("Please login first.")
        return

    _css()

    st.markdown(
        _h(
            """
            <div class="pf-title">My <span>Profile</span></div>
            <div class="pf-subtitle">Manage your account and session.</div>
            """
        ),
        unsafe_allow_html=True,
    )

    email_raw = getattr(user, "email", "") or "Not available"
    email = escape(email_raw)
    initial = escape(email_raw[0].upper()) if email_raw != "Not available" else "U"
    user_id = escape(str(user.id))
    since = escape(_member_since(user))

    stats = _load_stats(user)

    if stats is None:
        stats_html = ""
    else:
        total, avg, latest = stats
        stats_html = _h(
            f"""
            <div class="pf-label" style="margin-top:22px;">Your Activity</div>
            <div class="pf-stats">
                <div class="pf-stat">
                    <div class="pf-stat-num">{total}</div>
                    <div class="pf-stat-lbl">Analyses</div>
                </div>
                <div class="pf-stat">
                    <div class="pf-stat-num">{avg:.0f}</div>
                    <div class="pf-stat-lbl">Avg Score</div>
                </div>
                <div class="pf-stat">
                    <div class="pf-stat-num">{latest:.0f}</div>
                    <div class="pf-stat-lbl">Latest Score</div>
                </div>
            </div>
            """
        )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            _h(
                f"""
                <div class="pf-card">
                    <div class="pf-label">Account</div>
                    <div class="pf-head">
                        <div class="pf-avatar">{initial}</div>
                        <div style="min-width:0;">
                            <div class="pf-email">{email}</div>
                            <div class="pf-role">Member since {since}</div>
                        </div>
                    </div>
                    <div class="pf-field">
                        <div class="pf-field-lbl">Email</div>
                        <div class="pf-field-val">{email}</div>
                    </div>
                    <div class="pf-field">
                        <div class="pf-field-lbl">User ID</div>
                        <div class="pf-field-val">{user_id}</div>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            _h(
                f"""
                <div class="pf-card">
                    <div class="pf-label">Session</div>
                    <div class="pf-status"><span class="pf-dot"></span>Active session</div>
                    <div class="pf-text">
                        Your account is currently authenticated with Supabase.
                    </div>
                    {stats_html}
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    # ---------------- SIGN OUT ----------------

    st.markdown(
        _h(
            """
            <div class="pf-danger">
                <div class="pf-danger-title">🚪 Sign out</div>
                <div class="pf-text" style="margin-top:6px;">
                    Signing out will clear your current authentication session.
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="profile_logout",
    ):
        try:
            from frontend.services.supabase_client import logout_user

            logout_user()
        except Exception:
            pass

        # Clear local Streamlit session
        for key in [
            "user",
            "access_token",
            "refresh_token",
            "analysis_result",
            "selected_history_analysis",
        ]:
            st.session_state.pop(key, None)

        st.session_state["current_page"] = "home"
        st.session_state["auth_mode"] = "login"

        st.rerun()