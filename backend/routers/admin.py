from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import User, Department

router = APIRouter()


@router.get("/settings")
def admin_settings(current_user: User = Depends(get_current_user)):
    return {
        "company_id": current_user.company_id,
        "role": current_user.role,
        "theme": "light",
        "profile_complete": True,
    }


@router.get("/audit")
def audit_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"message": "Audit logs available", "user": current_user.full_name}
