from pathlib import Path
from .config import (
    COMPANY_DIR,
    USERS_DIR,
    SHARED_DIR,
)
def create_directory_structure():
    directories = [
        COMPANY_DIR / "Finance",
        COMPANY_DIR / "HR",
        COMPANY_DIR / "Internal",
        COMPANY_DIR / "Backups",
        COMPANY_DIR / "Projects" / "PaymentAPI",
        COMPANY_DIR / "Projects" / "InternalAI",
        COMPANY_DIR / "Projects" / "CustomerPortal",
        USERS_DIR / "admin",
        USERS_DIR / "developer",
        USERS_DIR / "finance",
        USERS_DIR / "hr",
        SHARED_DIR / "Documents",
        SHARED_DIR / "Reports",
        SHARED_DIR / "Software",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    print("[+] Deception filesystem created")
def create_fake_files():
    files = {
        COMPANY_DIR / "Finance" / "quarterly_report.txt":
            "Synthetic Q4 financial report.\nThis document contains fictional data.",
        COMPANY_DIR / "HR" / "employee_directory.txt":
            "Synthetic employee directory.\nAll identities are fictional.",
        COMPANY_DIR / "Internal" / "security_notes.txt":
            "Synthetic internal security notes.\nNo real credentials are stored.",
        COMPANY_DIR / "Projects" / "PaymentAPI" / "README.md":
            "# Payment API\nSynthetic payment processing project.",
        COMPANY_DIR / "Projects" / "InternalAI" / "README.md":
            "# Internal AI\nSynthetic internal AI research project.",
        COMPANY_DIR / "Projects" / "CustomerPortal" / "README.md":
            "# Customer Portal\nSynthetic customer portal project.",
        USERS_DIR / "developer" / "development_notes.txt":
            "Synthetic development notes.",
        USERS_DIR / "finance" / "finance_notes.txt":
            "Synthetic finance notes.",
        USERS_DIR / "admin" / "system_notes.txt":
            "Synthetic administrator notes.",
        SHARED_DIR / "Documents" / "company_policy.txt":
            "Synthetic company security policy.",
    }
    for file_path, content in files.items():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    print(f"[+] Created {len(files)} synthetic files")
def build_environment():
    create_directory_structure()
    create_fake_files()
    print("[+] Windows deception environment ready")