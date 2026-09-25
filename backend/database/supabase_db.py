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