from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DECOY_ROOT = BASE_DIR / "decoy"

COMPANY_DIR = DECOY_ROOT / "Company"
USERS_DIR = DECOY_ROOT / "Users"
SHARED_DIR = DECOY_ROOT / "Shared"

LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"