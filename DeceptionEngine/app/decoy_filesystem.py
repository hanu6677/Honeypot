from pathlib import Path
import json

from .events import record_event


BASE_DIR = Path(__file__).resolve().parent.parent / "decoy_environment"


DECoy_STRUCTURE = {
    "Company/HR": [
        "employee_directory.csv",
        "hr_policy.txt",
    ],
    "Company/Finance": [
        "quarterly_report.txt",
        "budget_summary.txt",
    ],
    "Company/Projects": [
        "project_alpha.txt",
        "project_beta.txt",
    ],
    "Company/Engineering": [
        "engineering_notes.txt",
        "deployment_plan.txt",
    ],
    "Repositories/payment-api": [
        "README.md",
        "config.example.json",
    ],
    "Repositories/internal-dashboard": [
        "README.md",
        "architecture.txt",
    ],
    "Backups": [
        "backup_manifest.json",
    ],
    "InternalAI": [
        "ai_project_notes.txt",
    ],
}


def create_decoy_environment():

    BASE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for directory, files in DECoy_STRUCTURE.items():

        directory_path = BASE_DIR / directory

        directory_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        for filename in files:

            file_path = directory_path / filename

            if file_path.exists():
                continue

            content = generate_content(filename)

            file_path.write_text(
                content,
                encoding="utf-8",
            )

    print(
        f"[+] Decoy environment created: {BASE_DIR}"
    )

    return BASE_DIR


def generate_content(filename):

    if filename.endswith(".csv"):

        return (
            "employee_id,name,department\n"
            "EMP-1001,Alex Carter,Engineering\n"
            "EMP-1002,Jordan Lee,Finance\n"
            "EMP-1003,Sam Wilson,HR\n"
        )

    if filename.endswith(".json"):

        data = {
            "environment": "synthetic",
            "status": "demo",
            "credentials": "NOT_REAL"
        }

        return json.dumps(
            data,
            indent=4,
        )

    if filename.endswith(".md"):

        return (
            "# Internal Repository\n\n"
            "Synthetic repository documentation.\n"
            "No real credentials or production secrets.\n"
        )

    return (
        "INTERNAL DECOY DOCUMENT\n\n"
        "This document contains synthetic "
        "honeypot information for security "
        "monitoring and research.\n"
    )