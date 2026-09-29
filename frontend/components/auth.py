import textwrap
import streamlit as st

from frontend.services.supabase_client import (
    sign_up_user,
    login_user,
)


def html(content: str) -> str:
    """Remove Python indentation before rendering HTML."""
    return textwrap.dedent(content).strip()


def render_auth():
    """Render login/signup authentication screen."""

    # ============================================================
    # AUTH PAGE CSS
    # ============================================================

    st.markdown(
        html(
            """
            <style>
                .auth-page {
                    max-width: 760px;
                    margin: 45px auto 0 auto;
                }

                .auth-brand {
                    text-align: center;
                    margin-bottom: 28px;
                }

                .auth-logo {
                    margin-bottom: 12px;
                }

                .auth-logo img {
                    width: 130px;
                    height: 130px;
                    object-fit: contain;
                }

                .auth-title {
                    font-size: 32px;
                    font-weight: 800;
                    color: #F8FAFC;
                    letter-spacing: -0.8px;
                }

                .auth-title span {
                    color: #A78BFA;
                }

                .auth-subtitle {
                    margin-top: 8px;
                    color: #94A3B8;
                    font-size: 14px;
                }

                .auth-card {
                    background:
                        linear-gradient(
                            145deg,
                            rgba(17,24,39,0.98),
                            rgba(15,23,42,0.98)
                        );

                    border: 1px solid rgba(139,92,246,0.25);

                    border-radius: 20px;

                    padding: 28px 30px;

                    box-shadow:
                        0 20px 60px rgba(0,0,0,0.28);
                }

                .auth-heading {
                    font-size: 25px;
                    font-weight: 750;
                    color: #F8FAFC;
                    margin-bottom: 6px;
                }

                .auth-description {
                    color: #64748B;
                    font-size: 13px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                }

                .auth-footer {
                    text-align: center;
                    margin-top: 22px;
                    color: #475569;
                    font-size: 12px;
                }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )

    # ============================================================
    # BRAND
    # ============================================================

    st.markdown(
        html(
            """
            <div class="auth-page">
                <div class="auth-brand">
                    <div class="auth-logo">
                        <img src="https://i.ibb.co/0gDd8CQ/bd78d6bd-b9a4-4162-85e3-4b3cc000acb2.png" alt="AI Resume ATS Logo">
                    </div>
                    <div class="auth-title">AI Resume <span>ATS</span></div>
                    <div class="auth-subtitle">Resume Intelligence Platform</div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ============================================================
    # LOGIN / SIGNUP TABS
    # ============================================================

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    mode = st.session_state["auth_mode"]

    # Active button ko highlight karne wala CSS
    active_key = "switch_login" if mode == "login" else "switch_signup"

    st.markdown(
        """
        <style>
            .st-key-switch_login button,
            .st-key-switch_signup button {
                height: 50px;
                border-radius: 999px !important;
                border: none !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                opacity: 0.45;
                transition: all 0.2s ease;
            }

            .st-key-switch_login button p,
            .st-key-switch_signup button p {
                color: #FFFFFF !important;
                font-size: 15px !important;
                font-weight: 700 !important;
            }

            /* Login button = purple/indigo */
            .st-key-switch_login button {
                background: linear-gradient(135deg, #8B5CF6, #6366F1) !important;
            }

            /* Create Account button = pink */
            .st-key-switch_signup button {
                background: linear-gradient(135deg, #EC4899, #F43F5E) !important;
            }

            .st-key-switch_login button:hover,
            .st-key-switch_signup button:hover {
                opacity: 0.85;
                transform: translateY(-1px);
            }

            .st-key-switch_login button:focus,
            .st-key-switch_signup button:focus {
                outline: none !important;
                box-shadow: none !important;
            }

            /* Active button */
            .st-key-ACTIVE button {
                opacity: 1 !important;
                box-shadow: 0 8px 24px rgba(139,92,246,0.45) !important;
            }
        </style>
        """.replace("ACTIVE", active_key),
        unsafe_allow_html=True,
    )

    col_login, col_signup = st.columns(2, gap="small")

    with col_login:
        if st.button(
            "🔐 Login",
            use_container_width=True,
            key="switch_login",
        ):
            st.session_state["auth_mode"] = "login"
            st.rerun()

    with col_signup:
        if st.button(
            "📝 Create Account",
            use_container_width=True,
            key="switch_signup",
        ):
            st.session_state["auth_mode"] = "signup"
            st.rerun()

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ============================================================
    # LOGIN
    # ============================================================

    if mode == "login":

        st.markdown(
            html(
                """
                <div class="auth-heading">
                    Welcome back
                </div>

                <div class="auth-description">
                    Sign in to analyze your resume and access
                    your analysis history.
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        login_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="auth_login_email",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="auth_login_password",
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary",
            key="auth_login_button",
        ):

            if not login_email.strip():

                st.error("Please enter your email.")

            elif not login_password:

                st.error("Please enter your password.")

            else:

                try:

                    response = login_user(
                        login_email.strip(),
                        login_password,
                    )

                    if response.user and response.session:

                        st.session_state["user"] = response.user

                        st.session_state["access_token"] = (
                            response.session.access_token
                        )

                        st.session_state["refresh_token"] = (
                            response.session.refresh_token
                        )

                        st.session_state["current_page"] = "home"

                        st.success("✅ Login successful!")

                        st.rerun()

                    else:

                        st.error(
                            "Login failed. Please check your credentials."
                        )

                except Exception as error:

                    st.error(
                        f"❌ Login failed: {error}"
                    )

    # ============================================================
    # SIGNUP
    # ============================================================

    else:

        st.markdown(
            html(
                """
                <div class="auth-heading">
                    Create your account
                </div>

                <div class="auth-description">
                    Create an account to analyze resumes and
                    save your analysis results.
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        signup_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="auth_signup_email",
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="auth_signup_password",
        )

        signup_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="auth_signup_confirm",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            type="primary",
            key="auth_signup_button",
        ):

            if not signup_email.strip():

                st.error("Please enter your email.")

            elif len(signup_password) < 8:

                st.error(
                    "Password must contain at least 8 characters."
                )

            elif signup_password != signup_confirm:

                st.error("Passwords do not match.")

            else:

                try:

                    response = sign_up_user(
                        signup_email.strip(),
                        signup_password,
                    )

                    if response.user:

                        if response.session:

                            st.session_state["user"] = (
                                response.user
                            )

                            st.session_state["access_token"] = (
                                response.session.access_token
                            )

                            st.session_state["refresh_token"] = (
                                response.session.refresh_token
                            )

                            st.session_state["current_page"] = "home"

                            st.success(
                                "✅ Account created successfully!"
                            )

                            st.rerun()

                        else:

                            st.success(
                                "✅ Account created successfully!"
                            )

                            st.info(
                                "Please check your email and "
                                "confirm your account before logging in."
                            )

                    else:

                        st.error(
                            "Account creation failed."
                        )

                except Exception as error:

                    st.error(
                        f"❌ Signup failed: {error}"
                    )

    # ============================================================
    # FOOTER
    # ============================================================

    st.markdown(
        html(
            """
            <div class="auth-footer">
                AI Resume ATS • Secure Resume Analysis
            </div>
            """
        ),
        unsafe_allow_html=True,
    )