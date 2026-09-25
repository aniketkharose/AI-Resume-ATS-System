from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        description="User password with minimum 8 characters",
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str | None = None


class AuthResponse(BaseModel):
    message: str
    user: UserResponse | None = None
    access_token: str | None = None
    refresh_token: str | None = None