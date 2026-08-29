from fastapi import FastAPI, Request
from .events import record_event
from .session import Session
from .data_generator import (
    generate_employee,
    generate_project,
    generate_ticket,
    generate_repository,
)
from .database.db import get_connection
app = FastAPI(
    title="Internal Company Portal",
    description="Deception HTTP Service",
)
SUSPICIOUS_ENDPOINTS = {
    "/admin": {
        "severity": "HIGH",
        "description": "Administrative endpoint probed",
    },
    "/backup": {
        "severity": "HIGH",
        "description": "Backup endpoint probed",
    },
    "/database": {
        "severity": "HIGH",
        "description": "Database endpoint probed",
    },
    "/config": {
        "severity": "HIGH",
        "description": "Configuration endpoint probed",
    },
}
@app.middleware("http")
async def deception_session(request: Request, call_next):
    # Create a session for this HTTP request
    client_ip = (
        request.client.host
        if request.client
        else "UNKNOWN"
    )
    session = Session(source=client_ip)
    # Store the session inside the request
    request.state.session = session

    # Basic request information
    method = request.method
    path = request.url.path
    user_agent = request.headers.get(
        "user-agent",
        "UNKNOWN"
    )
    endpoint_rule = SUSPICIOUS_ENDPOINTS.get(path)

    if endpoint_rule:
        record_event(
            event_type="SUSPICIOUS_ENDPOINT",
            description=endpoint_rule["description"],
            severity=endpoint_rule["severity"],
            session_id=session.session_id,
        )
    record_event(
        event_type="HTTP_REQUEST",
        description=(
            f"{method} {path} | "
            f"IP={client_ip} | "
            f"UA={user_agent}"
        ),
        severity="LOW",
        session_id=session.session_id,
    )
    try:
        response = await call_next(request)
        # Record the response
        record_event(
            event_type="HTTP_RESPONSE",
            description=(
                f"{method} {path} | "
                f"Status={response.status_code}"
            ),
            severity="LOW",
            session_id=session.session_id,
        )
        return response
    finally:
        session.end()
        record_event(
            event_type="SESSION_ENDED",
            description=f"HTTP session ended for {path}",
            severity="LOW",
            session_id=session.session_id,
        )
@app.get("/")
async def home(request: Request):
    session = request.state.session
    record_event(
        event_type="HTTP_ACCESS",
        description="Internal Company Portal accessed",
        severity="MEDIUM",
        session_id=session.session_id,
    )
    return {
        "service": "Internal Company Portal",
        "status": "online",
        "version": "2.4.1",
    }
@app.get("/api/status")
async def status(request: Request):
    session = request.state.session
    record_event(
        event_type="API_ACCESS",
        description="Status API accessed",
        severity="MEDIUM",
        session_id=session.session_id,
    )
    return {
        "database": "PostgreSQL",
        "environment": "production",
        "status": "healthy",
    }
@app.get("/internal")
async def internal(request: Request):
    session = request.state.session
    record_event(
        event_type="SENSITIVE_ENDPOINT_ACCESS",
        description="Internal endpoint accessed",
        severity="HIGH",
        session_id=session.session_id,
    )
    return {
        "message": "Internal company resources",
        "projects": [
            "PaymentAPI",
            "InternalAI",
            "CustomerPortal",
        ],
    }
@app.get("/admin")
async def admin(request: Request):
    session = request.state.session
    record_event(
        event_type="ADMIN_ACCESS",
        description="Fake administration panel accessed",
        severity="HIGH",
        session_id=session.session_id,
    )
    return {
        "application": "Internal Admin Portal",
        "status": "authenticated",
        "environment": "production",
    }
@app.get("/backup")
async def backup(request: Request):
    session = request.state.session
    record_event(
        event_type="BACKUP_ACCESS",
        description="Fake backup resource accessed",
        severity="HIGH",
        session_id=session.session_id,
    )
    return {
        "backup_system": "online",
        "latest_backup": "2026-08-24",
        "status": "available",
    }
@app.get("/database")
async def database(request: Request):
    session = request.state.session

    record_event(
        event_type="DATABASE_ACCESS",
        description="Fake database resource accessed",
        severity="HIGH",
        session_id=session.session_id,
    )

    return {
        "database": "PostgreSQL",
        "host": "db-internal",
        "status": "healthy",
    }
@app.get("/favicon.ico")
async def favicon(request: Request):
    session = request.state.session

    record_event(
        event_type="FAVICON_REQUEST",
        description="Browser requested favicon",
        severity="LOW",
        session_id=session.session_id,
    )
    return {}
@app.get("/employees")
async def employees(request: Request):
    session = request.state.session
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            employees.employee_id,
            employees.name,
            employees.email,
            employees.role,
            departments.name AS department
        FROM employees
        LEFT JOIN departments
            ON employees.department_id = departments.id
        ORDER BY employees.id
    """)
    rows = cursor.fetchall()
    connection.close()
    employees_data = [
        dict(row)
        for row in rows
    ]
    record_event(
        event_type="EMPLOYEE_DIRECTORY_ACCESS",
        description="Synthetic employee directory accessed",
        severity="MEDIUM",
        session_id=session.session_id,
    )
    return {
        "department": "Company Directory",
        "employees": employees_data,
    }
@app.get("/projects")
async def projects(request: Request):
    session = request.state.session
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            project_id,
            name,
            status,
            environment
        FROM projects
        ORDER BY id
    """)
    rows = cursor.fetchall()
    connection.close()
    projects_data = [
        dict(row)
        for row in rows
    ]
    record_event(
        event_type="PROJECT_DIRECTORY_ACCESS",
        description="Synthetic project directory accessed",
        severity="MEDIUM",
        session_id=session.session_id,
    )
    return {
        "projects": projects_data
    }
@app.get("/api/tickets")
async def tickets(request: Request):
    session = request.state.session
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            ticket_id,
            title,
            priority,
            status
        FROM tickets
        ORDER BY id
    """)
    rows = cursor.fetchall()
    connection.close()
    tickets_data = [
        dict(row)
        for row in rows
    ]
    record_event(
        event_type="TICKET_DATABASE_ACCESS",
        description="Synthetic support ticket data accessed",
        severity="MEDIUM",
        session_id=session.session_id,
    )
    return {
        "tickets": tickets_data
    }
@app.get("/api/repositories")
async def repositories(request: Request):
    session = request.state.session

    record_event(
        event_type="REPOSITORY_DISCOVERY",
        description="Synthetic internal repositories accessed",
        severity="HIGH",
        session_id=session.session_id,
    )

    return {
        "repositories": [
            generate_repository()
            for _ in range(5)
        ]
    }