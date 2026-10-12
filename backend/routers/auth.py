from datetime import datetime, date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import get_db
from .dependencies import get_current_user, require_roles
from .models import User, Company, Employee, Department, Project, ProjectMember, Task, TaskAssignment, Attendance, LeaveRequest, LeaveBalance, Lead, Notification, ActivityLog
from .security import get_password_hash, create_access_token
from .schemas import UserCreate, UserLogin, Token

router = APIRouter()


@router.post("/register", response_model=dict)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if payload.company_id is None:
        company = Company(name=f"{payload.full_name}'s Company", email=payload.email)
        db.add(company)
        db.flush()
        company_id = company.id
    else:
        company_id = payload.company_id

    user = User(
        company_id=company_id,
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()

    employee = Employee(
        company_id=company_id,
        user_id=user.id,
        employee_id=f"EMP-{user.id:04d}",
        email=payload.email,
        job_title="New Employee",
        joining_date=date.today(),
        status="Active",
    )
    db.add(employee)

    db.commit()
    db.refresh(user)
    return {"message": "Registration successful", "user_id": user.id, "company_id": company_id}


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    from .security import verify_password
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "role": user.role, "company_id": user.company_id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "company_id": current_user.company_id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
    }


@router.get("/users")
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_roles("Super Admin", "Company Admin"))):
    users = db.query(User).filter(User.company_id == current_user.company_id).all()
    return [{
        "id": u.id,
        "full_name": u.full_name,
        "email": u.email,
        "username": u.username,
        "role": u.role,
        "is_active": u.is_active,
    } for u in users]
