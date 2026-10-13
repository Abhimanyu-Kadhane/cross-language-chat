from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Message, User
from app.schemas import MessageCreate, MessageOut

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/text", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def send_text_message(
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Message:
    """Create a text message to an existing recipient."""
    recipient = db.get(User, payload.receiver_id)
    if recipient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")
    if recipient.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send a message to yourself")

    message = Message(
        sender_id=current_user.id,
        receiver_id=recipient.id,
        message_type="text",
        original_text=payload.text,
        original_language=current_user.preferred_language,
        translated_language=recipient.preferred_language,
        translated_text=None,
    )
    # PHASE 3: translate here
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/{other_user_id}", response_model=list[MessageOut])
def get_conversation(
    other_user_id: int,
    limit: int = Query(default=200, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Message]:
    """Return all messages in a one-to-one conversation, oldest first."""
    other_user = db.get(User, other_user_id)
    if other_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    messages = (
        db.query(Message)
        .filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other_user.id),
                and_(Message.sender_id == other_user.id, Message.receiver_id == current_user.id),
            )
        )
        .order_by(Message.created_at.desc(), Message.id.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages))
