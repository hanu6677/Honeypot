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
    connection.commit()
    connection.close()