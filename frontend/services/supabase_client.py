import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_PUBLISHABLE_KEY = os.getenv(
    "SUPABASE_PUBLISHABLE_KEY",
    "",
)


# ============================================================
# SUPABASE CLIENT
# ============================================================

def get_supabase_client() -> Client:
    """
    Create and return the Supabase client.
    """

    if not SUPABASE_URL:
        raise ValueError(
            "SUPABASE_URL is not configured."
        )

    if not SUPABASE_PUBLISHABLE_KEY:
        raise ValueError(
            "SUPABASE_PUBLISHABLE_KEY is not configured."
        )

    return create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY,
    )


# ============================================================
# SIGN UP
# ============================================================

def sign_up_user(
    email: str,
    password: str,
):
    """
    Create a new Supabase user.
    """

    if not email.strip():
        raise ValueError("Email is required.")

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    supabase = get_supabase_client()

    response = supabase.auth.sign_up(
        {
            "email": email.strip().lower(),
            "password": password,
        }
    )

    return response


# ============================================================
# LOGIN
# ============================================================

def login_user(
    email: str,
    password: str,
):
    """
    Login an existing Supabase user.
    """

    if not email.strip():
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

    return response


# ============================================================
# LOGOUT
# ============================================================

def logout_user():
    """
    Logout the current Supabase session.
    """

    supabase = get_supabase_client()

    supabase.auth.sign_out()


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():
    """
    Return the currently authenticated Supabase user.
    """

    supabase = get_supabase_client()

    response = supabase.auth.get_user()

    return response.user