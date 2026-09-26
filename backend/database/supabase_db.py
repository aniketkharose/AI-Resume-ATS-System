from supabase import create_client, Client

from backend.core.config import (
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY,
)


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client.

    The publishable key is used here because this client
    should respect Supabase authentication and RLS policies.
    """

    if not SUPABASE_URL:
        raise ValueError("SUPABASE_URL is not configured.")

    if not SUPABASE_PUBLISHABLE_KEY:
        raise ValueError("SUPABASE_PUBLISHABLE_KEY is not configured.")

    return create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY,
    )


def save_analysis(
    user_id: str,
    filename: str,
    ats_score: float,
    keyword_match: float,
    missing_keywords: list,
    analysis_result: dict,
    access_token: str,
    refresh_token: str,
) -> dict:
    """
    Save a completed resume analysis to Supabase
    using the authenticated user's session.
    """

    if not user_id:
        raise ValueError("User ID is required.")

    if not filename:
        raise ValueError("Filename is required.")

    if not access_token:
        raise ValueError("Access token is required.")

    if not refresh_token:
        raise ValueError("Refresh token is required.")

    # Create Supabase client
    supabase = get_supabase_client()

    # Attach the logged-in user's authentication session.
    # This is required for Supabase RLS policies.
    supabase.auth.set_session(
        access_token,
        refresh_token,
    )

    data = {
        "user_id": user_id,
        "filename": filename,
        "ats_score": ats_score,
        "keyword_match": keyword_match,
        "missing_keywords": missing_keywords,
        "analysis_result": analysis_result,
    }

    # Insert analysis into Supabase
    response = (
        supabase
        .table("analyses")
        .insert(data)
        .execute()
    )

    if not response.data:
        raise ValueError("Failed to save analysis.")

    return response.data[0]


def get_user_analyses(
    user_id: str,
    access_token: str,
    refresh_token: str,
) -> list:
    """
    Fetch analysis history for the authenticated user.

    Supabase RLS ensures that only the user's own
    analysis records can be returned.
    """

    if not user_id:
        raise ValueError("User ID is required.")

    if not access_token:
        raise ValueError("Access token is required.")

    if not refresh_token:
        raise ValueError("Refresh token is required.")

    # Create Supabase client
    supabase = get_supabase_client()

    # Attach authenticated user's session
    supabase.auth.set_session(
        access_token,
        refresh_token,
    )

    # Fetch user's analysis history
    response = (
        supabase
        .table("analyses")
        .select(
            "id, filename, ats_score, keyword_match, "
            "missing_keywords, analysis_result, created_at"
        )
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []