from __future__ import annotations

import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from .schemas import UserUpsert

LOCAL_USER_ID = "local-user"


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _resolve_sqlite_path(database_url: str) -> Path:
    if not database_url.startswith("sqlite:///"):
        raise ValueError("Only sqlite database URLs are supported for now")

    path_str = database_url.removeprefix("sqlite:///")
    path = Path(path_str)
    if not path.is_absolute():
        path = Path.cwd() / path

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _connect(database_url: str) -> sqlite3.Connection:
    path = _resolve_sqlite_path(database_url)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(database_url: str) -> None:
    with closing(_connect(database_url)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                trade_licensing_office TEXT NOT NULL,
                ico TEXT,
                dic TEXT,
                email TEXT,
                phone TEXT,
                bank TEXT,
                iban TEXT,
                swift TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        _ensure_columns(conn)
        conn.commit()


def _ensure_columns(conn: sqlite3.Connection) -> None:
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    if "company_name" in existing and "name" not in existing:
        conn.execute("ALTER TABLE users ADD COLUMN name TEXT")
        conn.execute("UPDATE users SET name = company_name WHERE name IS NULL")
        existing.add("name")
    expected = {
        "name": "TEXT",
        "address": "TEXT",
        "city": "TEXT",
        "country": "TEXT",
        "trade_licensing_office": "TEXT",
        "ico": "TEXT",
        "dic": "TEXT",
        "email": "TEXT",
        "phone": "TEXT",
        "bank": "TEXT",
        "iban": "TEXT",
        "swift": "TEXT",
        "created_at": "TEXT",
        "updated_at": "TEXT",
    }
    missing = [column for column in expected if column not in existing]
    for column in missing:
        _add_column(conn, column, expected)


def _add_column(conn: sqlite3.Connection, column: str, expected: dict[str, str]) -> None:
    if column not in expected:
        raise ValueError("Unexpected column requested for migration")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", column):
        raise ValueError("Invalid column name")
    conn.execute(f'ALTER TABLE users ADD COLUMN "{column}" {expected[column]}')


def _row_to_user(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "address": row["address"],
        "city": row["city"],
        "country": row["country"],
        "trade_licensing_office": row["trade_licensing_office"],
        "ico": row["ico"],
        "dic": row["dic"],
        "email": row["email"],
        "phone": row["phone"],
        "bank": row["bank"],
        "iban": row["iban"],
        "swift": row["swift"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _is_complete_user(user: dict) -> bool:
    required_fields = ("name", "address", "city", "country", "trade_licensing_office")
    for field in required_fields:
        value = user.get(field)
        if not isinstance(value, str) or not value.strip():
            return False
    return True


def get_user(database_url: str) -> dict | None:
    with closing(_connect(database_url)) as conn:
        row = conn.execute(
            """
            SELECT
                id,
                name,
                address,
                city,
                country,
                trade_licensing_office,
                ico,
                dic,
                email,
                phone,
                bank,
                iban,
                swift,
                created_at,
                updated_at
            FROM users
            WHERE id = ?
            """,
            (LOCAL_USER_ID,),
        ).fetchone()

    if not row:
        return None

    user = _row_to_user(row)
    if not _is_complete_user(user):
        return None
    return user


def upsert_user(database_url: str, payload: UserUpsert) -> dict:
    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        conn.execute(
            """
            INSERT INTO users (
                id,
                name,
                address,
                city,
                country,
                trade_licensing_office,
                ico,
                dic,
                email,
                phone,
                bank,
                iban,
                swift,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                address = excluded.address,
                city = excluded.city,
                country = excluded.country,
                trade_licensing_office = excluded.trade_licensing_office,
                ico = excluded.ico,
                dic = excluded.dic,
                email = excluded.email,
                phone = excluded.phone,
                bank = excluded.bank,
                iban = excluded.iban,
                swift = excluded.swift,
                updated_at = excluded.updated_at
            """,
            (
                LOCAL_USER_ID,
                payload.name,
                payload.address,
                payload.city,
                payload.country,
                payload.trade_licensing_office,
                payload.ico,
                payload.dic,
                payload.email,
                payload.phone,
                payload.bank,
                payload.iban,
                payload.swift,
                now,
                now,
            ),
        )
        conn.commit()

    user = get_user(database_url)
    if not user:
        raise RuntimeError("Failed to load user profile")

    return user
