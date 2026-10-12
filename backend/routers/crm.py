from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import User, Lead

router = APIRouter()


@router.get("/")
def list_leads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    leads = db.query(Lead).filter(Lead.company_id == current_user.company_id).all()
    return [{
        "id": l.id,
        "name": l.name,
        "email": l.email,
        "phone": l.phone,
        "company_name": l.company_name,
        "stage": l.stage,
        "value": l.value,
    } for l in leads]


@router.post("/")
def create_lead(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lead = Lead(
        company_id=current_user.company_id,
        name=payload["name"],
        email=payload.get("email"),
        phone=payload.get("phone"),
        company_name=payload.get("company_name"),
        source=payload.get("source"),
        stage=payload.get("stage", "New"),
        value=payload.get("value", 0),
        assigned_to=payload.get("assigned_to"),
        follow_up_date=payload.get("follow_up_date"),
        notes=payload.get("notes"),
    )
    db.add(lead)
    db.commit()
    return {"message": "Lead created", "id": lead.id}
