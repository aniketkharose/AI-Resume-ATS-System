import streamlit as st
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# COMPONENTS
# ============================================================

from frontend.components.auth import render_auth
from frontend.components.sidebar import render_sidebar


# ============================================================
# VIEWS
# ============================================================

from frontend.views.home import render_home
from frontend.views.analyze import render_analyze
from frontend.views.history import render_history
from frontend.views.analysis_detail import render_analysis_detail
from frontend.views.profile import render_profile


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume ATS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 85% -10%,
                rgba(124,58,237,0.10),
                transparent 30%
            ),
            #0B0F19;

        color: #F8FAFC;
    }


    .block-container {

        max-width: 1200px;

        padding-top: 1.5rem;

        padding-bottom: 3rem;
    }


    /* =====================================================
       BUTTONS (main area)
    ===================================================== */

    div.stButton > button {

        min-height: 44px !important;

        border-radius: 11px !important;

        font-weight: 650 !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease !important;
    }


    div.stButton > button:hover {

        transform: translateY(-2px) !important;

        box-shadow:
            0 10px 28px rgba(0,0,0,0.25) !important;
    }


    /* =====================================================
       PRIMARY BUTTON
    ===================================================== */

    div.stButton > button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                #8B5CF6,
                #6366F1
            ) !important;

        color: #FFFFFF !important;

        border:
            1px solid rgba(167,139,250,0.45) !important;

        box-shadow:
            0 8px 24px rgba(99,102,241,0.20) !important;
    }


    div.stButton > button[kind="primary"]:hover {

        background:
            linear-gradient(
                135deg,
                #9F67FF,
                #7068FF
            ) !important;

        box-shadow:
            0 14px 34px rgba(99,102,241,0.35) !important;
    }


    /* =====================================================
       NORMAL BUTTON
    ===================================================== */

    div.stButton > button:not([kind="primary"]) {

        background:
            linear-gradient(
                180deg,
                #151A27,
                #111622
            ) !important;

        color: #E2E8F0 !important;
    }


    div.stButton > button:not([kind="primary"]):hover {

        background:
            linear-gradient(
                180deg,
                #1B2030,
                #151A27
            ) !important;

        border-color:
            rgba(139,92,246,0.42) !important;
    }


    /* =====================================================
       INPUTS
    ===================================================== */

    div[data-baseweb="input"] {

        background: #111827 !important;

        border-radius: 10px !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;
    }


    div[data-baseweb="input"]:focus-within {

        border-color:
            rgba(139,92,246,0.55) !important;

        box-shadow:
            0 0 0 1px rgba(139,92,246,0.20) !important;
    }


    textarea {

        background: #111827 !important;

        border-radius: 12px !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        color: #F8FAFC !important;
    }


    textarea:focus {

        border-color:
            rgba(139,92,246,0.55) !important;
    }


    /* =====================================================
       FILE UPLOADER
    ===================================================== */

    [data-testid="stFileUploader"] {

        background: #111827;

        border-radius: 14px;

        border:
            1px solid rgba(255,255,255,0.08);

        padding: 8px;
    }


    /* =====================================================
       METRICS
    ===================================================== */

    [data-testid="stMetric"] {

        background: #111827;

        border:
            1px solid rgba(255,255,255,0.07);

        border-radius: 16px;

        padding: 16px;
    }


    /* =====================================================
       HEADINGS
    ===================================================== */

    h1,
    h2,
    h3 {

        color: #F8FAFC !important;
    }


    /* =====================================================
       DIVIDERS
    ===================================================== */

    hr {

        border-color:
            rgba(255,255,255,0.08) !important;
    }


    /* =====================================================
       STREAMLIT UI
    ===================================================== */

    #MainMenu {
        visibility: hidden;
    }


    footer {
        visibility: hidden;
    }


    header {
        background: transparent !important;
    }


    /* =====================================================
       SCROLLBAR
    ===================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }


    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }


    ::-webkit-scrollbar-thumb {

        background: #2B3040;

        border-radius: 10px;
    }


    ::-webkit-scrollbar-thumb:hover {

        background: #4C3A78;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "user" not in st.session_state:
    st.session_state["user"] = None

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"


# ============================================================
# AUTHENTICATION
# ============================================================

if st.session_state["user"] is None:

    render_auth()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar()


# ============================================================
# PAGE ROUTING
# ============================================================

current_page = st.session_state["current_page"]


if current_page == "home":

    render_home()


elif current_page == "analyze":

    render_analyze()


elif current_page == "history":

    render_history()


elif current_page == "analysis_detail":

    render_analysis_detail()


elif current_page == "profile":

    render_profile()


else:

    st.session_state["current_page"] = "home"

    render_home()