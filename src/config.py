"""Application-wide configuration constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "kpi_dashboard.db"

SESSION_EXPIRY_HOURS = 24
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15

ROLES = ["admin", "manager", "viewer"]

DATA_DIR.mkdir(parents=True, exist_ok=True)
