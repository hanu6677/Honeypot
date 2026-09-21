from datetime import datetime, timedelta
import hashlib
from .db import get_connection
DEPARTMENTS = [
    "Engineering",
    "Security",
    "Finance",
    "Operations",
    "Data",
]
EMPLOYEES = [
    (
        "EMP-1042",
        "Aarav Sharma",
        "aarav.sharma@example-corp.local",
        "Engineering",
        "Software Engineer",
    ),
    (
        "EMP-1087",
        "Neha Kapoor",
        "neha.kapoor@example-corp.local",
        "Security",
        "Security Analyst",
    ),
    (
        "EMP-1134",
        "Rohan Mehta",
        "rohan.mehta@example-corp.local",
        "Operations",
        "DevOps Engineer",
    ),
    (
        "EMP-1178",
        "Isha Verma",
        "isha.verma@example-corp.local",
        "Data",
        "Database Administrator",
    ),
    (
        "EMP-1203",
        "Kabir Singh",
        "kabir.singh@example-corp.local",
        "Finance",
        "Financial Analyst",
    ),
]
PROJECTS = [
    (
        "PRJ-1001",
        "PaymentAPI",
        "active",
        "production",
    ),
    (
        "PRJ-1002",
        "InternalAI",
        "development",
        "development",
    ),
    (
        "PRJ-1003",
        "CustomerPortal",
        "active",
        "production",
    ),
    (
        "PRJ-1004",
        "FraudDetection",
        "development",
        "staging",
    ),
]
TICKETS = [
    (
        "TKT-10021",
        "Payment API latency",
        "high",
        "investigating",
    ),
    (
        "TKT-10022",
        "Database connection issue",
        "medium",
        "open",
    ),
    (
        "TKT-10023",
        "Internal authentication failure",
        "high",
        "investigating",
    ),
]
REPOSITORIES = [
    (
        "repo-payment-api",
        "payment-api",
        "PRJ-1001",
        "internal",
        "main",
    ),
    (
        "repo-internal-ai",
        "internal-ai",
        "PRJ-1002",
        "internal",
        "develop",
    ),
    (
        "repo-customer-portal",
        "customer-portal",
        "PRJ-1003",
        "internal",
        "main",
    ),
    (
        "repo-fraud-engine",
        "fraud-engine",
        "PRJ-1004",
        "internal",
        "develop",
    ),
]
COMMIT_MESSAGES = [
    "Initial project structure",
    "Update API validation",
    "Fix database connection handling",
    "Improve authentication middleware",
    "Add monitoring support",
]
def seed_database():
    connection = get_connection()
    cursor = connection.cursor()
    # Departments
    for department in DEPARTMENTS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO departments (name)
            VALUES (?)
            """,
            (department,),
        )
    # Employees
    for employee in EMPLOYEES:
        employee_id, name, email, department, role = employee
        cursor.execute(
            "SELECT id FROM departments WHERE name = ?",
            (department,),
        )
        department_row = cursor.fetchone()
        if department_row:
            department_id = department_row["id"]

            cursor.execute(
                """
                INSERT OR IGNORE INTO employees
                (
                    employee_id,
                    name,
                    email,
                    department_id,
                    role
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    employee_id,
                    name,
                    email,
                    department_id,
                    role,
                ),
            )
    # Projects
    for project in PROJECTS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO projects
            (
                project_id,
                name,
                status,
                environment
            )
            VALUES (?, ?, ?, ?)
            """,
            project,
        )
    # Tickets
    for ticket in TICKETS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO tickets
            (
                ticket_id,
                title,
                priority,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            ticket,
        )

        # Repositories

    for repository in REPOSITORIES:

        repository_id, name, project_code, visibility, branch = repository

        cursor.execute(
            """
            SELECT id
            FROM projects
            WHERE project_id = ?
            """,
            (project_code,),
        )

        project = cursor.fetchone()

        if project:

            cursor.execute(
                """
                INSERT OR IGNORE INTO repositories
                (
                    repository_id,
                    name,
                    project_id,
                    visibility,
                    branch
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    repository_id,
                    name,
                    project["id"],
                    visibility,
                    branch,
                ),
            )
                # Synthetic commits

    cursor.execute("""
        SELECT
            repositories.id,
            repositories.name
        FROM repositories
    """)

    repositories = cursor.fetchall()

    for repository in repositories:

        for index, message in enumerate(COMMIT_MESSAGES):

            commit_hash = hashlib.sha1(
                f"{repository['name']}-{index}".encode()
            ).hexdigest()[:10]

            created_at = (
                datetime.now()
                - timedelta(days=30 - index * 5)
            ).isoformat()

            cursor.execute(
                """
                INSERT OR IGNORE INTO commits
                (
                    commit_hash,
                    repository_id,
                    author,
                    message,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    commit_hash,
                    repository["id"],
                    "Aarav Sharma",
                    message,
                    created_at,
                ),
            )
    connection.commit()
    connection.close()