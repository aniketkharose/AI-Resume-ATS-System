import textwrap
from html import escape

import streamlit as st


LOGO_URL = "https://i.ibb.co/0gDd8CQ/bd78d6bd-b9a4-4162-85e3-4b3cc000acb2.png"

NAV_ITEMS = [
    ("home", "🏠  Home", "nav_home"),
    ("analyze", "📄  Analyze Resume", "nav_analyze"),
    ("history", "📊  Analysis History", "nav_history"),
    ("profile", "👤  Profile", "nav_profile"),
]


def html(content: str) -> str:
    """Remove Python indentation before rendering HTML."""
    return textwrap.dedent(content).strip()


def _active_page(current_page: str) -> str:
    # Analysis detail page par "History" highlighted rahe
    if current_page == "analysis_detail":
        return "history"
    return current_page


def _sidebar_css(active_page: str) -> str:
    active_key = next(
        (key for page, _, key in NAV_ITEMS if page == active_page),
        "nav_home",
    )

    return """
    <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F1220 0%, #141827 100%) !important;
            border-right: 1px solid rgba(139,92,246,0.15) !important;
        }

        /* ---------- Brand ---------- */
        .sb-brand {
            text-align: center;
            padding: 6px 0 18px 0;
        }
        .sb-brand img {
            width: 76px;
            height: 76px;
            object-fit: contain;
            margin-bottom: 8px;
            filter: drop-shadow(0 6px 18px rgba(139,92,246,0.35));
        }
        .sb-title {
            font-size: 20px;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -0.4px;
        }
        .sb-title span { color: #A78BFA; }
        .sb-subtitle {
            margin-top: 4px;
            font-size: 11px;
            color: #64748B;
            letter-spacing: 0.4px;
        }

        .sb-label {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #475569;
            margin: 6px 0 8px 6px;
        }

        /* ---------- Nav buttons ---------- */
        section[data-testid="stSidebar"] [class*="st-key-nav_"] button {
            min-height: 46px !important;
            border-radius: 12px !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            justify-content: flex-start !important;
            padding-left: 14px !important;
            transition: all 0.2s ease !important;
        }
        section[data-testid="stSidebar"] [class*="st-key-nav_"] button > div {
            justify-content: flex-start !important;
        }
        section[data-testid="stSidebar"] [class*="st-key-nav_"] button p {
            color: #94A3B8 !important;
            font-size: 14.5px !important;
            font-weight: 600 !important;
            text-align: left !important;
        }
        section[data-testid="stSidebar"] [class*="st-key-nav_"] button:hover {
            background: rgba(139,92,246,0.10) !important;
            border-color: rgba(139,92,246,0.25) !important;
            transform: translateX(3px) !important;
        }
        section[data-testid="stSidebar"] [class*="st-key-nav_"] button:hover p {
            color: #F8FAFC !important;
        }

        /* ---------- Active page ---------- */
        section[data-testid="stSidebar"] .st-key-ACTIVE button {
            background: linear-gradient(
                135deg,
                rgba(139,92,246,0.30),
                rgba(99,102,241,0.18)
            ) !important;
            border: 1px solid rgba(139,92,246,0.55) !important;
            box-shadow: 0 8px 22px rgba(99,102,241,0.22) !important;
        }
        section[data-testid="stSidebar"] .st-key-ACTIVE button p {
            color: #FFFFFF !important;
        }

        /* ---------- User card ---------- */
        .sb-user {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            border-radius: 14px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            margin-bottom: 10px;
        }
        .sb-avatar {
            width: 38px;
            height: 38px;
            flex-shrink: 0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: #FFFFFF;
            background: linear-gradient(135deg, #8B5CF6, #6366F1);
        }
        .sb-user-info { min-width: 0; }
        .sb-user-label {
            font-size: 10px;
            color: #64748B;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }
        .sb-user-email {
            font-size: 12.5px;
            color: #E2E8F0;
            font-weight: 600;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* ---------- Logout ---------- */
        section[data-testid="stSidebar"] .st-key-nav_logout button {
            min-height: 42px !important;
            border-radius: 12px !important;
            background: rgba(239,68,68,0.08) !important;
            border: 1px solid rgba(239,68,68,0.30) !important;
            justify-content: center !important;
        }
        section[data-testid="stSidebar"] .st-key-nav_logout button p {
            color: #FCA5A5 !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] .st-key-nav_logout button:hover {
            background: rgba(239,68,68,0.18) !important;
            transform: none !important;
        }
    </style>
    """.replace("ACTIVE", active_key)


def render_sidebar():
    """Render premium sidebar navigation."""

    current_page = st.session_state.get("current_page", "home")
    active_page = _active_page(current_page)

    st.markdown(_sidebar_css(active_page), unsafe_allow_html=True)

    with st.sidebar:

        # ---------------- Brand ----------------
        st.markdown(
            html(
                f"""
                <div class="sb-brand">
                    <img src="{LOGO_URL}" alt="Logo">
                    <div class="sb-title">AI Resume <span>ATS</span></div>
                    <div class="sb-subtitle">Resume Intelligence Platform</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        # ---------------- Navigation ----------------
        st.markdown('<div class="sb-label">MENU</div>', unsafe_allow_html=True)

        for page, label, key in NAV_ITEMS:
            if st.button(label, use_container_width=True, key=key):
                st.session_state["current_page"] = page
                st.rerun()

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # ---------------- User card ----------------
        user = st.session_state.get("user")

        if user:
            email = escape(getattr(user, "email", "") or "User")
            initial = email[0].upper()

            st.markdown(
                html(
                    f"""
                    <div class="sb-user">
                        <div class="sb-avatar">{initial}</div>
                        <div class="sb-user-info">
                            <div class="sb-user-label">Signed in as</div>
                            <div class="sb-user-email">{email}</div>
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

            if st.button("🚪  Logout", use_container_width=True, key="nav_logout"):
                st.session_state["user"] = None
                st.session_state["access_token"] = None
                st.session_state["refresh_token"] = None
                st.session_state["current_page"] = "home"
                st.rerun()