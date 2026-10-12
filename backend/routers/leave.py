from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import User, LeaveRequest

router = APIRouter()


@router.get("/")
def list_leave_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    leaves = db.query(LeaveRequest).filter(LeaveRequest.company_id == current_user.company_id).all()
    return [{
        "id": l.id,
        "employee_id": l.employee_id,
        "leave_type": l.leave_type,
        "start_date": l.start_date.isoformat(),
        "end_date": l.end_date.isoformat(),
        "status": l.status,
        "reason": l.reason,
    } for l in leaves]


@router.post("/")
def create_leave_request(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    leave = LeaveRequest(
        company_id=current_user.company_id,
        employee_id=payload["employee_id"],
        leave_type=payload["leave_type"],
        start_date=payload["start_date"],
        end_date=payload["end_date"],
        reason=payload.get("reason"),
        status="Pending",
    )
    db.add(leave)
    db.commit()
    return {"message": "Leave request created", "id": leave.id}


@router.patch("/{leave_id}/status")
def update_leave_status(leave_id: int, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.company_id == current_user.company_id, LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    leave.status = payload.get("status", leave.status)
    leave.manager_comment = payload.get("manager_comment")
    db.commit()
    return {"message": "Leave status updated"}
