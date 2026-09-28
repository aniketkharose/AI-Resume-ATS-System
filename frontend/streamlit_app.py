import streamlit as st
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
from frontend.services.supabase_client import (
    sign_up_user,
    login_user,
    logout_user,
)

# ============================================================
# BACKEND SERVICES
# ============================================================
from frontend.views.history import render_history
from frontend.views.analysis_detail import render_analysis_detail
from frontend.views.analyze import render_analyze
from frontend.views.home import render_home
from frontend.views.profile import render_profile

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume ATS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        "📄 Analyze Resume",
        use_container_width=True,
    ):
        st.session_state["current_page"] = "analyze"
        st.rerun()
    
    if st.button(
        "📊 Analysis History",
        use_container_width=True,
    ):
        st.session_state["current_page"] = "history"
        st.rerun()

    if st.button(
        "👤 Profile",
        use_container_width=True,
    ):
        st.session_state["current_page"] = "profile"
        st.rerun()
        
    st.markdown("---")

    user = st.session_state.get("user")

    if user:
        st.caption(
            f"Signed in as\n{user.email}"
        )

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

    .hero-badge {
        display: block;
        width: fit-content;
        margin: 70px auto 22px auto;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.30);
        color: #c4b5fd;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .hero-title {
        text-align: center;
        font-size: 4rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -2px;
        color: #ffffff;
        margin: 0;
    }

    .hero-title span {
        color: #8b5cf6;
    }

    .hero-description {
        max-width: 720px;
        margin: 22px auto 0 auto;
        text-align: center;
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
# PAGE ROUTING
# ============================================================
if st.session_state["current_page"] == "analyze":
    render_analyze()
    st.stop()

if st.session_state["current_page"] == "history":

    render_history()

    st.stop()


if st.session_state["current_page"] == "analysis_detail":

    render_analysis_detail()

    st.stop()

if st.session_state["current_page"] == "home":
    render_home()
    st.stop()

if st.session_state["current_page"] == "profile":
    render_profile()
    st.stop()

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