from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import Company, Department, User

router = APIRouter()


@router.get("/")
def list_departments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    departments = db.query(Department).filter(Department.company_id == current_user.company_id).all()
    return [{
        "id": d.id,
        "name": d.name,
        "description": d.description,
    } for d in departments]


@router.post("/")
def create_department(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    department = Department(company_id=current_user.company_id, name=payload["name"], description=payload.get("description"))
    db.add(department)
    db.commit()
    return {"message": "Department created", "id": department.id}
