from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import User, Notification

router = APIRouter()


@router.get("/")
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    return [{
        "id": item.id,
        "title": item.title,
        "message": item.message,
        "type": item.type,
        "is_read": item.is_read,
    } for item in items]


@router.patch("/{notification_id}/read")
def mark_notification_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Notification).filter(Notification.user_id == current_user.id, Notification.id == notification_id).first()
    if item:
        item.is_read = True
        db.commit()
    return {"message": "Notification marked as read"}
