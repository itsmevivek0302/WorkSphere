from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import User, Project, ProjectMember, Employee, Task

router = APIRouter()


@router.get("/")
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.company_id == current_user.company_id).all()
    return [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "status": p.status,
        "priority": p.priority,
        "progress": p.progress,
    } for p in projects]


@router.post("/")
def create_project(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = Project(
        company_id=current_user.company_id,
        name=payload["name"],
        description=payload.get("description"),
        status=payload.get("status", "Active"),
        priority=payload.get("priority", "Medium"),
        progress=payload.get("progress", 0),
    )
    db.add(project)
    db.commit()
    return {"message": "Project created", "id": project.id}


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.company_id == current_user.company_id, Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "priority": project.priority,
        "progress": project.progress,
    }
