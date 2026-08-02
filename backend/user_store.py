"""
User account persistence for DermaTwin AI.

Stores local signups and generic OAuth-style provider logins in backend/users.json.
"""

import json
import secrets
import hashlib
import hmac
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from models import UserAccount

USERS_FILE = Path(__file__).parent / "users.json"
_USERS: dict[str, UserAccount] = {}


def _normalize_user_id(user_id: str) -> str:
    return user_id.strip().lower()


def _find_by_email(email: Optional[str]) -> Optional[UserAccount]:
    if not email:
        return None
    for user in _USERS.values():
        if user.email and user.email.lower() == email.lower():
            return user
    return None


def _find_by_provider(provider: str, oauth_id: Optional[str]) -> Optional[UserAccount]:
    if not oauth_id:
        return None
    for user in _USERS.values():
        if user.provider == provider and user.oauth_id == oauth_id:
            return user
    return None


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 150000).hex()


def _build_salt() -> bytes:
    return secrets.token_bytes(16)


def _serialize_user(user: UserAccount) -> dict:
    return user.model_dump()


def load_users() -> None:
    global _USERS
    if not USERS_FILE.exists():
        _USERS = {}
        return
    try:
        raw = json.loads(USERS_FILE.read_text(encoding="utf-8"))
        users = raw.get("users", []) if isinstance(raw, dict) else []
        _USERS = {}
        for item in users:
            account = UserAccount.model_validate(item)
            _USERS[_normalize_user_id(account.user_id)] = account
    except Exception:
        _USERS = {}


def save_users() -> None:
    USERS_FILE.write_text(
        json.dumps({"users": [_serialize_user(user) for user in _USERS.values()]}, indent=2),
        encoding="utf-8",
    )


def get_user(user_id: str) -> Optional[UserAccount]:
    return _USERS.get(_normalize_user_id(user_id))


def list_users() -> list[UserAccount]:
    return list(_USERS.values())


def create_local_user(
    user_id: str,
    email: str,
    password: str,
    full_name: Optional[str] = None,
    city: Optional[str] = None,
    allergies: Optional[list[str]] = None,
) -> UserAccount:
    normalized_id = _normalize_user_id(user_id)
    if normalized_id in _USERS:
        raise ValueError("user_id already exists")
    if _find_by_email(email):
        raise ValueError("email already exists")
    salt = _build_salt()
    password_hash = _hash_password(password, salt)
    account = UserAccount(
        user_id=normalized_id,
        email=email,
        full_name=full_name,
        provider="local",
        password_hash=password_hash,
        password_salt=salt.hex(),
        oauth_id=None,
        city=city,
        allergies=allergies or [],
        created_at=datetime.now(timezone.utc).isoformat(),
        is_active=True,
    )
    _USERS[normalized_id] = account
    save_users()
    return account


def authenticate_local_user(
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> UserAccount:
    account = None
    if user_id:
        account = get_user(user_id)
    if not account and email:
        account = _find_by_email(email)
    if not account:
        raise ValueError("No account found for that user_id or email")
    if account.provider != "local" or not account.password_hash or not account.password_salt:
        raise ValueError("Password login is not supported for this account")
    expected = _hash_password(password or "", bytes.fromhex(account.password_salt))
    if not hmac.compare_digest(expected, account.password_hash):
        raise ValueError("Invalid password")
    return account


def _build_unique_user_id(base: str) -> str:
    normalized = _normalize_user_id(base)
    candidate = normalized
    suffix = 1
    while candidate in _USERS:
        candidate = f"{normalized}-{suffix}"
        suffix += 1
    return candidate


def create_oauth_user(
    provider: str,
    oauth_id: Optional[str] = None,
    email: Optional[str] = None,
    full_name: Optional[str] = None,
    city: Optional[str] = None,
    allergies: Optional[list[str]] = None,
) -> UserAccount:
    if oauth_id:
        existing = _find_by_provider(provider, oauth_id)
        if existing:
            return existing
    if email:
        existing = _find_by_email(email)
        if existing and existing.provider == provider:
            return existing
    if not email and not oauth_id:
        raise ValueError("OAuth login requires an email or oauth_id")
    base = email.split("@")[0] if email else f"{provider}-{oauth_id}"
    user_id = _build_unique_user_id(base)
    account = UserAccount(
        user_id=user_id,
        email=email,
        full_name=full_name,
        provider=provider,
        password_hash=None,
        password_salt=None,
        oauth_id=oauth_id,
        city=city,
        allergies=allergies or [],
        created_at=datetime.now(timezone.utc).isoformat(),
        is_active=True,
    )
    _USERS[user_id] = account
    save_users()
    return account


load_users()
