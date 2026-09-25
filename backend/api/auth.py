from typing import Any

from backend.database.supabase_db import get_supabase_client


def sign_up_user(email: str, password: str) -> dict[str, Any]:
    """
    Create a new user using Supabase Email/Password authentication.
    """

    if not email or not email.strip():
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    supabase = get_supabase_client()

    response = supabase.auth.sign_up(
        {
            "email": email.strip().lower(),
            "password": password,
        }
    )

    return {
        "user": response.user,
        "session": response.session,
    }


def login_user(email: str, password: str) -> dict[str, Any]:
    """
    Authenticate an existing user using Email/Password.
    """

    if not email or not email.strip():
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    supabase = get_supabase_client()

    response = supabase.auth.sign_in_with_password(
        {
            "email": email.strip().lower(),
            "password": password,
        }
    )

    return {
        "user": response.user,
        "session": response.session,
    }


def logout_user() -> None:
    """
    Sign out the current Supabase authentication session.
    """

    supabase = get_supabase_client()
    supabase.auth.sign_out()


def get_current_user(access_token: str):
    """
    Verify an access token and return the authenticated user.
    """

    if not access_token:
        raise ValueError("Access token is required.")

    supabase = get_supabase_client()

    response = supabase.auth.get_user(access_token)

    if not response.user:
        raise ValueError("Invalid or expired access token.")

    return response.user