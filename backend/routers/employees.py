from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import get_db
from .dependencies import get_current_user
from .models import Employee, Department, User, Project, Task

router = APIRouter()


@router.get("/")
def list_employees(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), q: str = Query(None), department_id: int = Query(None), status: str = Query(None), skip: int = 0, limit: int = 50):
    query = db.query(Employee).filter(Employee.company_id == current_user.company_id)
    if q:
        query = query.filter(Employee.email.ilike(f"%{q}%"))
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    if status:
        query = query.filter(Employee.status == status)
    employees = query.offset(skip).limit(limit).all()
    return [{
        "id": e.id,
        "employee_id": e.employee_id,
        "full_name": e.user.full_name if e.user else e.email,
        "email": e.email,
        "job_title": e.job_title,
        "department_id": e.department_id,
        "status": e.status,
        "manager_id": e.manager_id,
        "joining_date": e.joining_date.isoformat(),
    } for e in employees]


@router.post("/")
def create_employee(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not payload.get("full_name"):
        raise HTTPException(status_code=400, detail="Name is required")
    user = User(
        company_id=current_user.company_id,
        email=payload["email"],
        username=payload.get("username", payload["email"].split("@")[0]),
        full_name=payload["full_name"],
        password_hash="hashed-user-password",
        role="Employee",
    )
    db.add(user)
    db.flush()
    emp = Employee(
        company_id=current_user.company_id,
        user_id=user.id,
        employee_id=payload.get("employee_id", f"EMP-{user.id:04d}"),
        department_id=payload.get("department_id"),
        manager_id=payload.get("manager_id"),
        job_title=payload.get("job_title", "Employee"),
        email=payload["email"],
        phone=payload.get("phone"),
        joining_date=payload.get("joining_date"),
        status=payload.get("status", "Active"),
    )
    db.add(emp)
    db.commit()
    return {"message": "Employee created"}


@router.get("/{employee_id}")
def fetch_employee(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.company_id == current_user.company_id, Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "full_name": employee.user.full_name if employee.user else employee.email,
        "email": employee.email,
        "job_title": employee.job_title,
        "status": employee.status,
        "department_id": employee.department_id,
        "manager_id": employee.manager_id,
    }
