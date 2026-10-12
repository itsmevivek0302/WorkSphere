from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .database import get_db
from .dependencies import get_current_user
from .models import User, Attendance, Employee

router = APIRouter()


@router.get("/")
def list_attendance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(Attendance).filter(Attendance.company_id == current_user.company_id).all()
    return [{
        "id": r.id,
        "employee_id": r.employee_id,
        "date": r.date.isoformat(),
        "check_in": r.check_in.isoformat() if r.check_in else None,
        "check_out": r.check_out.isoformat() if r.check_out else None,
        "working_hours": r.working_hours,
    } for r in records]


@router.post("/check-in")
def check_in(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.company_id == current_user.company_id, Employee.id == payload["employee_id"]).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    existing = db.query(Attendance).filter(Attendance.employee_id == employee.id, Attendance.date == payload.get("date")).first()
    if existing and existing.check_in:
        raise HTTPException(status_code=400, detail="Already checked in")
    record = existing or Attendance(company_id=current_user.company_id, employee_id=employee.id, date=payload.get("date"))
    record.check_in = datetime.utcnow()
    if not existing:
        db.add(record)
    db.commit()
    return {"message": "Check in recorded"}


@router.post("/check-out")
def check_out(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(Attendance).filter(Attendance.company_id == current_user.company_id, Attendance.employee_id == payload["employee_id"], Attendance.date == payload.get("date")).first()
    if not record or not record.check_in:
        raise HTTPException(status_code=400, detail="Check in is required")
    if record.check_out:
        raise HTTPException(status_code=400, detail="Already checked out")
    record.check_out = datetime.utcnow()
    delta = record.check_out - record.check_in
    record.working_hours = round(delta.total_seconds() / 3600, 2)
    db.commit()
    return {"message": "Check out recorded", "working_hours": record.working_hours}
