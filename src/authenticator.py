"""Authentication and session management."""

import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import streamlit as st

from src.database import get_connection, init_db, log_audit
from src.config import (
    SESSION_EXPIRY_HOURS,
    MAX_LOGIN_ATTEMPTS,
    LOGIN_LOCKOUT_MINUTES,
)

JWT_SECRET = "default_jwt_secret_change_in_production"
try:
    JWT_SECRET = st.secrets["auth"]["jwt_secret"]
except Exception:
    pass

_login_attempts: dict[str, list[datetime]] = {}


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"), hashed.encode("utf-8")
    )


def _is_rate_limited(identifier: str) -> bool:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=LOGIN_LOCKOUT_MINUTES)
    if identifier in _login_attempts:
        _login_attempts[identifier] = [
            t for t in _login_attempts[identifier] if t > cutoff
        ]
        if len(_login_attempts[identifier]) >= MAX_LOGIN_ATTEMPTS:
            return True
    return False


def _record_attempt(identifier: str):
    now = datetime.now(timezone.utc)
    _login_attempts.setdefault(identifier, []).append(now)


def _create_token(
    user_id: str, email: str, role: str, views: str
) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "permitted_views": views,
        "exp": datetime.now(timezone.utc)
        + timedelta(hours=SESSION_EXPIRY_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def ensure_admin_exists():
    init_db()
    with get_connection() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            uid = str(uuid.uuid4())
            pw = _hash_password("admin123")
            conn.execute(
                "INSERT INTO users "
                "(user_id,email,password_hash,role,"
                "permitted_views,is_active,created_at) "
                "VALUES (?,?,?,?,?,?,?)",
                (
                    uid, "admin@company.com", pw, "admin",
                    '["ceo","sales","finance"]', 1,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )


def login(email: str, password: str) -> tuple[bool, str]:
    if _is_rate_limited(email):
        return (
            False,
            f"Too many attempts. Wait {LOGIN_LOCKOUT_MINUTES} min.",
        )
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT user_id, password_hash, role, "
            "permitted_views, is_active "
            "FROM users WHERE email=?",
            (email,),
        )
        row = cur.fetchone()
    if not row:
        _record_attempt(email)
        return False, "Invalid email or password."
    uid, pw_hash, role, views, active = row
    if not active:
        return False, "Account deactivated."
    if not _verify_password(password, pw_hash):
        _record_attempt(email)
        return False, "Invalid email or password."
    token = _create_token(uid, email, role, views)
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET last_login=? WHERE user_id=?",
            (datetime.now(timezone.utc).isoformat(), uid),
        )
    log_audit(uid, "login", f"Login: {email}")
    return True, token


def get_current_user() -> dict | None:
    token = st.session_state.get("auth_token")
    if not token:
        return None
    try:
        return jwt.decode(
            token, JWT_SECRET, algorithms=["HS256"]
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
