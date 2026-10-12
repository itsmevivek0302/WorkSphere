from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import Employee, Department, User, Project, Task, Attendance, LeaveRequest, Lead, Notification, ActivityLog

router = APIRouter()


@router.get("/overview")
def dashboard_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company_id = current_user.company_id
    total_employees = db.query(Employee).filter(Employee.company_id == company_id).count()
    total_projects = db.query(Project).filter(Project.company_id == company_id).count()
    pending_tasks = db.query(Task).filter(Task.company_id == company_id, Task.status != "Completed").count()
    completed_tasks = db.query(Task).filter(Task.company_id == company_id, Task.status == "Completed").count()
    active_leaves = db.query(LeaveRequest).filter(LeaveRequest.company_id == company_id, LeaveRequest.status == "Pending").count()
    recent_activity = db.query(ActivityLog).filter(ActivityLog.company_id == company_id).order_by(ActivityLog.created_at.desc()).limit(8).all()
    attendance_today = db.query(Attendance).filter(Attendance.company_id == company_id).count()

    return {
        "stats": {
            "total_employees": total_employees,
            "active_projects": total_projects,
            "tasks_completed": completed_tasks,
            "tasks_pending": pending_tasks,
            "attendance_today": attendance_today,
            "pending_leave_requests": active_leaves,
        },
        "recent_activity": [
            {
                "id": item.id,
                "entity_type": item.entity_type,
                "action": item.action,
                "details": item.details,
                "created_at": item.created_at.isoformat(),
            }
            for item in recent_activity
        ],
    }
