from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.languages import SUPPORTED_LANGUAGES, is_supported_language
from app.models import User
from app.schemas import LanguageOut, LanguageUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])
public_router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)) -> User:
    """Fetch the authenticated user's profile."""
    return current_user


@router.patch("/me/language", response_model=UserOut)
def update_user_language(
    payload: LanguageUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Update the authenticated user's preferred language."""
    current_user.preferred_language = payload.preferred_language
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("", response_model=list[UserOut])
def list_users(
    search: str | None = Query(default=None, description="Case-insensitive username search"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[User]:
    """List all users except the authenticated account, ordered alphabetically."""
    query = db.query(User).filter(User.id != current_user.id)

    if search and search.strip():
        search_term = search.strip().lower()
        query = query.filter(func.lower(User.username).contains(search_term))

    users = query.order_by(User.username.asc()).all()
    return users


@public_router.get("/languages", response_model=list[LanguageOut])
def get_supported_languages() -> list[LanguageOut]:
    """Return the list of supported languages for client-side selection."""
    return [LanguageOut(code=code, name=name) for code, name in SUPPORTED_LANGUAGES.items()]
