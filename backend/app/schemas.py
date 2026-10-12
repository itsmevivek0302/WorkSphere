from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    company_id: Optional[int] = None


class CompanyCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CompanyOut(BaseModel):
    id: int
    name: str
    domain: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    company_id: Optional[int] = None
    role: str = "Employee"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    company_id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department_id: Optional[int] = None
    job_title: str
    manager_id: Optional[int] = None
    joining_date: date
    phone: Optional[str] = None
    status: str = "Active"


class EmployeeOut(BaseModel):
    id: int
    company_id: int
    user_id: int
    employee_id: str
    department_id: Optional[int]
    manager_id: Optional[int]
    job_title: str
    email: str
    phone: Optional[str]
    joining_date: date
    status: str


class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentOut(BaseModel):
    id: int
    company_id: int
    name: str
    description: Optional[str]


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "Active"
    priority: str = "Medium"
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    manager_id: Optional[int] = None


class ProjectOut(BaseModel):
    id: int
    company_id: int
    name: str
    description: Optional[str]
    status: str
    priority: str
    start_date: Optional[date]
    due_date: Optional[date]
    manager_id: Optional[int]
    progress: float


class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    status: str = "Todo"
    priority: str = "Medium"
    due_date: Optional[date] = None
    assignee_ids: List[int] = []


class TaskOut(BaseModel):
    id: int
    company_id: int
    project_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[date]


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None


class CRMLeadCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    source: Optional[str] = None
    stage: str = "New"
    value: float = 0
    assigned_to: Optional[int] = None
    follow_up_date: Optional[date] = None
    notes: Optional[str] = None


class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime


class ActivityLogOut(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    action: str
    details: Optional[str]
    created_at: datetime
