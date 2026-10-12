from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, dashboard, employees, departments, projects, tasks, attendance, leave, crm, notifications, admin, reports
from .seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WorkSphere API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(departments.router, prefix="/api/departments", tags=["departments"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["attendance"])
app.include_router(leave.router, prefix="/api/leave", tags=["leave"])
app.include_router(crm.router, prefix="/api/crm", tags=["crm"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.on_event("startup")
def startup_event():
    seed_data()

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "WorkSphere"}
