from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from .schemas import ClientCreate, ClientUpdate


class EmailConflictError(Exception):
    pass


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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                email TEXT NOT NULL,
                notes TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS clients_email_active_idx
            ON clients (lower(email))
            WHERE deleted_at IS NULL
            """
        )
        conn.commit()


def _row_to_client(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "address": row["address"],
        "email": row["email"],
        "notes": row["notes"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def list_clients(database_url: str) -> list[dict]:
    with closing(_connect(database_url)) as conn:
        rows = conn.execute(
            """
            SELECT id, name, address, email, notes, created_at, updated_at
            FROM clients
            WHERE deleted_at IS NULL
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [_row_to_client(row) for row in rows]


def get_client(database_url: str, client_id: int) -> dict | None:
    with closing(_connect(database_url)) as conn:
        row = conn.execute(
            """
            SELECT id, name, address, email, notes, created_at, updated_at
            FROM clients
            WHERE id = ? AND deleted_at IS NULL
            """,
            (client_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_client(row)


def email_in_use(database_url: str, email: str, exclude_id: int | None = None) -> bool:
    with closing(_connect(database_url)) as conn:
        if exclude_id is None:
            row = conn.execute(
                """
                SELECT 1
                FROM clients
                WHERE lower(email) = lower(?) AND deleted_at IS NULL
                """,
                (email,),
            ).fetchone()
        else:
            row = conn.execute(
                """
                SELECT 1
                FROM clients
                WHERE lower(email) = lower(?) AND deleted_at IS NULL AND id != ?
                """,
                (email, exclude_id),
            ).fetchone()

    return row is not None


def create_client(database_url: str, payload: ClientCreate) -> dict:
    if email_in_use(database_url, payload.email):
        raise EmailConflictError()

    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO clients (name, address, email, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.name,
                    payload.address,
                    payload.email,
                    payload.notes,
                    now,
                    now,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            raise EmailConflictError() from exc

        client_id = cursor.lastrowid

    created = get_client(database_url, int(client_id))
    if not created:
        raise RuntimeError("Failed to load created client")

    return created


def update_client(database_url: str, client_id: int, payload: ClientUpdate) -> dict | None:
    if email_in_use(database_url, payload.email, exclude_id=client_id):
        raise EmailConflictError()

    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        try:
            cursor = conn.execute(
                """
                UPDATE clients
                SET name = ?, address = ?, email = ?, notes = ?, updated_at = ?
                WHERE id = ? AND deleted_at IS NULL
                """,
                (
                    payload.name,
                    payload.address,
                    payload.email,
                    payload.notes,
                    now,
                    client_id,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            raise EmailConflictError() from exc

        if cursor.rowcount == 0:
            return None

    return get_client(database_url, client_id)


def soft_delete_client(database_url: str, client_id: int) -> bool:
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
