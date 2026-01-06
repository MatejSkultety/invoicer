from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from .schemas import ClientCreate, ClientUpdate


def _utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


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
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                main_contact_method TEXT NOT NULL,
                main_contact TEXT NOT NULL,
                additional_contact TEXT,
                ico TEXT,
                dic TEXT,
                notes TEXT,
                favourite INTEGER NOT NULL DEFAULT 0,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT
            )
            """
        )
        conn.commit()


def _row_to_client(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "address": row["address"],
        "city": row["city"],
        "country": row["country"],
        "main_contact_method": row["main_contact_method"],
        "main_contact": row["main_contact"],
        "additional_contact": row["additional_contact"],
        "ico": row["ico"],
        "dic": row["dic"],
        "notes": row["notes"],
        "favourite": bool(row["favourite"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def list_clients(database_url: str) -> list[dict]:
    with closing(_connect(database_url)) as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                name,
                address,
                city,
                country,
                main_contact_method,
                main_contact,
                additional_contact,
                ico,
                dic,
                notes,
                favourite,
                created_at,
                updated_at
            FROM clients
            WHERE deleted_at IS NULL
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [_row_to_client(row) for row in rows]


def get_client(database_url: str, client_id: str) -> dict | None:
    with closing(_connect(database_url)) as conn:
        row = conn.execute(
            """
            SELECT
                id,
                name,
                address,
                city,
                country,
                main_contact_method,
                main_contact,
                additional_contact,
                ico,
                dic,
                notes,
                favourite,
                created_at,
                updated_at
            FROM clients
            WHERE id = ? AND deleted_at IS NULL
            """,
            (client_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_client(row)


def create_client(database_url: str, payload: ClientCreate) -> dict:
    now = _utc_now()
    created_by = _current_user()
    client_id = str(uuid4())
    with closing(_connect(database_url)) as conn:
        cursor = conn.execute(
            """
            INSERT INTO clients (
                id,
                name,
                address,
                city,
                country,
                main_contact_method,
                main_contact,
                additional_contact,
                ico,
                dic,
                notes,
                favourite,
                created_by,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                client_id,
                payload.name,
                payload.address,
                payload.city,
                payload.country,
                payload.main_contact_method.value,
                payload.main_contact,
                payload.additional_contact,
                payload.ico,
                payload.dic,
                payload.notes,
                int(payload.favourite),
                created_by,
                now,
                now,
            ),
        )
        conn.commit()

    created = get_client(database_url, client_id)
    if not created:
        raise RuntimeError("Failed to load created client")

    return created


def update_client(database_url: str, client_id: str, payload: ClientUpdate) -> dict | None:
    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        cursor = conn.execute(
            """
            UPDATE clients
            SET
                name = ?,
                address = ?,
                city = ?,
                country = ?,
                main_contact_method = ?,
                main_contact = ?,
                additional_contact = ?,
                ico = ?,
                dic = ?,
                notes = ?,
                favourite = ?,
                updated_at = ?
            WHERE id = ? AND deleted_at IS NULL
            """,
            (
                payload.name,
                payload.address,
                payload.city,
                payload.country,
                payload.main_contact_method.value,
                payload.main_contact,
                payload.additional_contact,
                payload.ico,
                payload.dic,
                payload.notes,
                int(payload.favourite),
                now,
                client_id,
            ),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None

    return get_client(database_url, client_id)


def soft_delete_client(database_url: str, client_id: str) -> bool:
    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        cursor = conn.execute(
            """
            UPDATE clients
            SET deleted_at = ?, updated_at = ?
            WHERE id = ? AND deleted_at IS NULL
            """,
            (now, now, client_id),
        )
        conn.commit()

    return cursor.rowcount > 0


def _current_user() -> str:
    """Return the current user identifier for audit fields.

    TODO: replace this stub with real user context once auth is available.
    The future implementation should derive the user from the request context
    (or equivalent service layer) and avoid hardcoded defaults.
    """
    return "dev"
