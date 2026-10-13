import re
from datetime import datetime

from email_validator import EmailNotValidError
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.languages import SUPPORTED_LANGUAGES, is_supported_language

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")


class UserCreate(BaseModel):
    """Input schema for creating a new user."""

    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    preferred_language: str = "en"

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        return str(value).strip().lower()

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.fullmatch(value):
            raise ValueError("Username must be 3 to 30 characters and contain only letters, digits, or underscores.")
        return value

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8 or len(value) > 72:
            raise ValueError("Password must be between 8 and 72 characters long.")
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise ValueError("Password must contain at least one letter and one digit.")
        return value

    @field_validator("preferred_language")
    @classmethod
    def validate_preferred_language(cls, value: str) -> str:
        normalized = str(value).strip().lower()
        if not is_supported_language(normalized):
            valid_languages = ", ".join(sorted(SUPPORTED_LANGUAGES))
            raise ValueError(f"Preferred language must be one of the supported codes: {valid_languages}")
        return normalized


class UserLogin(BaseModel):
    """Input schema for authentication."""

    username: str
    password: str


class UserOut(BaseModel):
    """Public user information returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    preferred_language: str
    created_at: datetime


class LanguageUpdate(BaseModel):
    """Schema used to update a user's preferred language."""

    preferred_language: str

    @field_validator("preferred_language")
    @classmethod
    def validate_preferred_language(cls, value: str) -> str:
        normalized = str(value).strip().lower()
        if not is_supported_language(normalized):
            valid_languages = ", ".join(sorted(SUPPORTED_LANGUAGES))
            raise ValueError(f"Preferred language must be one of the supported codes: {valid_languages}")
        return normalized


class Token(BaseModel):
    """JWT token response payload."""

    access_token: str
    token_type: str = "bearer"
    user: UserOut


class LanguageOut(BaseModel):
    """Language metadata exposed to clients."""

    code: str
    name: str
