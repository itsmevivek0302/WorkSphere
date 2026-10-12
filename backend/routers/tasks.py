from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import User, Task, TaskAssignment, Employee

router = APIRouter()


@router.get("/")
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.company_id == current_user.company_id).all()
    return [{
        "id": t.id,
        "project_id": t.project_id,
        "title": t.title,
        "status": t.status,
        "priority": t.priority,
        "description": t.description,
        "due_date": t.due_date.isoformat() if t.due_date else None,
    } for t in tasks]


@router.post("/")
def create_task(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = Task(
        company_id=current_user.company_id,
        project_id=payload["project_id"],
        title=payload["title"],
        description=payload.get("description"),
        status=payload.get("status", "Todo"),
        priority=payload.get("priority", "Medium"),
        due_date=payload.get("due_date"),
    )
    db.add(task)
    db.flush()
    for assignee_id in payload.get("assignee_ids", []):
        db.add(TaskAssignment(task_id=task.id, employee_id=assignee_id))
    db.commit()
    return {"message": "Task created", "id": task.id}


@router.patch("/{task_id}")
def update_task(task_id: int, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.company_id == current_user.company_id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.items():
        if hasattr(task, key):
            setattr(task, key, value)
    db.commit()
    return {"message": "Task updated"}
