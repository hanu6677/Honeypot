import random
import uuid
from datetime import datetime, timedelta
FIRST_NAMES = [
    "Advait",
    "Mohit",
    "Arjun",
    "Kabir",
    "Vihaan",
    "Aditya",
    "Neha",
    "Ananya",
    "Priya",
    "Isha",
]
LAST_NAMES = [
    "Sharma",
    "Verma",
    "Kapoor",
    "Mehta",
    "Malhotra",
    "Singh",
    "Patel",
    "Kumar",
]
DEPARTMENTS = [
    "Engineering",
    "Security",
    "Finance",
    "Operations",
    "Data",
]
PROJECTS = [
    "PaymentAPI",
    "InternalAI",
    "CustomerPortal",
    "FraudDetection",
    "CloudMigration",
]
def generate_employee():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return {
        "employee_id": f"EMP-{random.randint(1000, 9999)}",
        "name": f"{first} {last}",
        "email": f"{first.lower()}.{last.lower()}@example-corp.local",
        "department": random.choice(DEPARTMENTS),
        "role": random.choice([
            "Software Engineer",
            "Security Analyst",
            "DevOps Engineer",
            "Database Administrator",
            "System Administrator",
        ]),
    }
def generate_project():
    return {
        "project_id": f"PRJ-{random.randint(1000, 9999)}",
        "name": random.choice(PROJECTS),
        "status": random.choice([
            "active",
            "development",
            "maintenance",
        ]),
        "environment": random.choice([
            "development",
            "staging",
            "production",
        ]),
    }
def generate_ticket():
    return {
        "ticket_id": f"TKT-{random.randint(10000, 99999)}",
        "title": random.choice([
            "Payment API latency",
            "Database connection issue",
            "Internal authentication failure",
            "Deployment problem",
            "Monitoring alert",
        ]),
        "priority": random.choice([
            "low",
            "medium",
            "high",
        ]),
        "status": random.choice([
            "open",
            "investigating",
            "resolved",
        ]),
    }
def generate_repository():
    return {
        "repository_id": str(uuid.uuid4())[:8],
        "name": random.choice([
            "payment-api",
            "customer-portal",
            "internal-ai",
            "fraud-engine",
            "security-monitor",
        ]),
        "visibility": "internal",
        "branch": random.choice([
            "main",
            "develop",
            "release",
        ]),
        "last_commit": (
            datetime.now() - timedelta(
                minutes=random.randint(1, 5000)
            )
        ).isoformat(),
    }