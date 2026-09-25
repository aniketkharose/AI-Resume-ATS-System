from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.api.auth import login_user, sign_up_user, get_current_user
from backend.models.schemas import (
    AuthResponse,
    LoginRequest,
    SignupRequest,
    UserResponse,
)

security = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(request: SignupRequest):
    """
    Register a new user using Supabase Email/Password authentication.
    """

    try:
        result = sign_up_user(
            email=request.email,
            password=request.password,
        )

        user = result["user"]
        session = result["session"]

        return AuthResponse(
            message="Account created successfully. Please verify your email.",
            user=(
                UserResponse(
                    id=str(user.id),
                    email=user.email,
                )
                if user
                else None
            ),
            access_token=session.access_token if session else None,
            refresh_token=session.refresh_token if session else None,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(request: LoginRequest):
    """
    Authenticate an existing user using Supabase Email/Password authentication.
    """

    try:
        result = login_user(
            email=request.email,
            password=request.password,
        )

        user = result["user"]
        session = result["session"]

        return AuthResponse(
            message="Login successful.",
            user=(
                UserResponse(
                    id=str(user.id),
                    email=user.email,
                )
                if user
                else None
            ),
            access_token=session.access_token if session else None,
            refresh_token=session.refresh_token if session else None,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

@router.get("/me", response_model=UserResponse)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Return the currently authenticated user.
    """

    try:
        user = get_current_user(credentials.credentials)

        return UserResponse(
            id=str(user.id),
            email=user.email,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )