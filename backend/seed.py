from datetime import date
import random
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import Company, User, Employee, Department, Project, ProjectMember, Task, TaskAssignment, Attendance, LeaveRequest, Lead, Notification, ActivityLog
from backend.app.security import get_password_hash


def seed_data():
    db: Session = SessionLocal()
    try:
        if db.query(Company).count() > 0:
            return

        company = Company(name="Northwind Labs", domain="northwindlabs.com", email="hello@northwindlabs.com")
        db.add(company)
        db.flush()

        admin = User(
            company_id=company.id,
            email="admin@northwindlabs.com",
            username="admin",
            full_name="Alicia Morgan",
            password_hash=get_password_hash("admin123"),
            role="Super Admin",
        )
        db.add(admin)
        db.flush()

        dept1 = Department(company_id=company.id, name="Engineering")
        dept2 = Department(company_id=company.id, name="Sales")
        dept3 = Department(company_id=company.id, name="HR")
        db.add_all([dept1, dept2, dept3])
        db.flush()

        emp1 = Employee(
            company_id=company.id,
            user_id=admin.id,
            employee_id="EMP-1001",
            department_id=dept1.id,
            email="admin@northwindlabs.com",
            job_title="Platform Lead",
            joining_date=date(2023, 1, 10),
            status="Active",
        )
        db.add(emp1)
        db.flush()

        user2 = User(company_id=company.id, email="jane@northwindlabs.com", username="jane", full_name="Jane Scott", password_hash=get_password_hash("admin123"), role="Manager")
        db.add(user2)
        db.flush()
        emp2 = Employee(company_id=company.id, user_id=user2.id, employee_id="EMP-1002", department_id=dept1.id, manager_id=emp1.id, email="jane@northwindlabs.com", job_title="Engineering Manager", joining_date=date(2022, 4, 12), status="Active")
        db.add(emp2)
        db.flush()

        user3 = User(company_id=company.id, email="omar@northwindlabs.com", username="omar", full_name="Omar Ali", password_hash=get_password_hash("admin123"), role="Employee")
        db.add(user3)
        db.flush()
        emp3 = Employee(company_id=company.id, user_id=user3.id, employee_id="EMP-1003", department_id=dept1.id, manager_id=emp2.id, email="omar@northwindlabs.com", job_title="Frontend Engineer", joining_date=date(2024, 2, 24), status="Active")
        db.add(emp3)
        db.flush()

        project = Project(company_id=company.id, name="WorkSphere SaaS Launch", description="Main SaaS rollout", status="Active", priority="High", progress=58)
        db.add(project)
        db.flush()

        db.add(ProjectMember(project_id=project.id, employee_id=emp1.id, role="Owner"))
        db.add(ProjectMember(project_id=project.id, employee_id=emp2.id, role="Manager"))
        db.add(ProjectMember(project_id=project.id, employee_id=emp3.id, role="Member"))

        task1 = Task(company_id=company.id, project_id=project.id, title="Design dashboard UI", status="In Progress", priority="High", description="Finalize SaaS dashboard")
        task2 = Task(company_id=company.id, project_id=project.id, title="Set up authentication", status="Review", priority="High")
        task3 = Task(company_id=company.id, project_id=project.id, title="Prepare onboarding docs", status="Todo", priority="Medium")
        db.add_all([task1, task2, task3])
        db.flush()

        db.add_all([
            TaskAssignment(task_id=task1.id, employee_id=emp3.id),
            TaskAssignment(task_id=task2.id, employee_id=emp2.id),
            TaskAssignment(task_id=task3.id, employee_id=emp2.id),
        ])

        db.add(Attendance(company_id=company.id, employee_id=emp2.id, date=date.today(), check_in=date.today().strftime('%Y-%m-%d') + ' 09:00:00', check_out=date.today().strftime('%Y-%m-%d') + ' 17:30:00', working_hours=8.5))
        db.add(LeaveRequest(company_id=company.id, employee_id=emp3.id, leave_type="Annual", start_date=date(2026, 10, 20), end_date=date(2026, 10, 22), status="Pending"))
        db.add(Lead(company_id=company.id, name="Northstar Ventures", email="hello@northstar.com", stage="Qualified", value=15000, source="Referral"))
        db.add(Notification(company_id=company.id, user_id=admin.id, title="Project update", message="WorkSphere SaaS Launch moved to review", type="project"))
        db.add(ActivityLog(company_id=company.id, user_id=admin.id, entity_type="project", entity_id=project.id, action="updated", details="Project milestone completed"))

        db.commit()
    finally:
        db.close()
