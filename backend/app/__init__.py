from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, dashboard, employees, departments, projects, tasks, attendance, leave, crm, notifications, admin, reports
from .seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WorkSphere API", docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [auth.router, dashboard.router, employees.router, departments.router, projects.router, tasks.router, attendance.router, leave.router, crm.router, notifications.router, admin.router, reports.router]:
    match router:
        case auth.router:
            app.include_router(auth.router, prefix="/api/auth")
        case dashboard.router:
            app.include_router(dashboard.router, prefix="/api/dashboard")
        case employees.router:
            app.include_router(employees.router, prefix="/api/employees")
        case departments.router:
            app.include_router(departments.router, prefix="/api/departments")
        case projects.router:
            app.include_router(projects.router, prefix="/api/projects")
        case tasks.router:
            app.include_router(tasks.router, prefix="/api/tasks")
        case attendance.router:
            app.include_router(attendance.router, prefix="/api/attendance")
        case leave.router:
            app.include_router(leave.router, prefix="/api/leave")
        case crm.router:
            app.include_router(crm.router, prefix="/api/crm")
        case notifications.router:
            app.include_router(notifications.router, prefix="/api/notifications")
        case admin.router:
            app.include_router(admin.router, prefix="/api/admin")
        case reports.router:
            app.include_router(reports.router, prefix="/api/reports")

@app.on_event("startup")
def startup_event():
    seed_data()

@app.get("/health")
def health():
    return {"status": "ok"}
