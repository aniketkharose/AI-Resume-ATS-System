import streamlit as st


def render_profile():

    user = st.session_state.get("user")

    if not user:
        st.warning("Please login first.")
        return

    st.title("👤 Profile")
    st.caption("Manage your account and session.")

    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Account")

            st.write("**Email**")
            st.write(user.email or "Not available")

            st.write("**User ID**")
            st.code(str(user.id))

    with col2:
        with st.container(border=True):
            st.subheader("Session")

            st.success("🟢 Active session")

            st.write(
                "Your account is currently authenticated "
                "with Supabase."
            )

    st.divider()

    st.subheader("🚪 Sign out")

    st.caption(
        "Signing out will clear your current authentication session."
    )

    if st.button(
        "🚪 Logout",
        type="primary",
        use_container_width=True,
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

        st.success("Logged out successfully.")
        st.rerun()