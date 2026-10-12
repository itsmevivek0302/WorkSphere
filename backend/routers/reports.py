from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import get_db
from .dependencies import get_current_user
from .models import User, Employee, Project, Task, LeaveRequest, Lead, Attendance

router = APIRouter()


@router.get("/summary")
def reports_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company_id = current_user.company_id
    return {
        "employees": db.query(Employee).filter(Employee.company_id == company_id).count(),
        "projects": db.query(Project).filter(Project.company_id == company_id).count(),
        "tasks": db.query(Task).filter(Task.company_id == company_id).count(),
        "leave_requests": db.query(LeaveRequest).filter(LeaveRequest.company_id == company_id).count(),
        "leads": db.query(Lead).filter(Lead.company_id == company_id).count(),
        "attendance_records": db.query(Attendance).filter(Attendance.company_id == company_id).count(),
    }
