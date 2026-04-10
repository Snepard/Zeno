"""
JSON-based User Store — replaces PostgreSQL user table.
Users are stored in storage/users.json.
"""
import json
import uuid
import threading
from pathlib import Path
import bcrypt

STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)
USERS_FILE = STORAGE_DIR / "users.json"

_lock = threading.Lock()


def _load() -> dict:
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def get_user_by_email(email: str) -> dict | None:
    with _lock:
        users = _load()
    for u in users.values():
        if u["email"] == email:
            return u
    return None


def get_user_by_id(user_id: str) -> dict | None:
    with _lock:
        users = _load()
    return users.get(user_id)


def create_user(email: str, password: str, full_name: str = "") -> dict:
    if get_user_by_email(email):
        raise ValueError("Email already registered")
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "hashed_password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
    }
    with _lock:
        users = _load()
        users[user_id] = user
        _save(users)
    return user


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False
