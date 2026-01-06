from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .schemas import CatalogItemCreate, CatalogItemUpdate


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
            CREATE TABLE IF NOT EXISTS catalog_items (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                unit TEXT NOT NULL,
                unit_price INTEGER NOT NULL,
                tax_rate INTEGER,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT
            )
            """
        )
        conn.commit()


def _row_to_catalog_item(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "unit": row["unit"],
        "unit_price": row["unit_price"],
        "tax_rate": row["tax_rate"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def list_catalog_items(database_url: str) -> list[dict]:
    with closing(_connect(database_url)) as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                name,
                description,
                unit,
                unit_price,
                tax_rate,
                created_at,
                updated_at
            FROM catalog_items
            WHERE deleted_at IS NULL
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [_row_to_catalog_item(row) for row in rows]


def get_catalog_item(database_url: str, item_id: str) -> dict | None:
    with closing(_connect(database_url)) as conn:
        row = conn.execute(
            """
            SELECT
                id,
                name,
                description,
                unit,
                unit_price,
                tax_rate,
                created_at,
                updated_at
            FROM catalog_items
            WHERE id = ? AND deleted_at IS NULL
            """,
            (item_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_catalog_item(row)


def create_catalog_item(database_url: str, payload: CatalogItemCreate) -> dict:
    now = _utc_now()
    created_by = _current_user()
    item_id = str(uuid4())
    with closing(_connect(database_url)) as conn:
        conn.execute(
            """
            INSERT INTO catalog_items (
                id,
                name,
                description,
                unit,
                unit_price,
                tax_rate,
                created_by,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                payload.name,
                payload.description,
                payload.unit,
                payload.unit_price,
                payload.tax_rate,
                created_by,
                now,
                now,
            ),
        )
        conn.commit()

    created = get_catalog_item(database_url, item_id)
    if not created:
        raise RuntimeError("Failed to load created catalog item")

    return created


def update_catalog_item(database_url: str, item_id: str, payload: CatalogItemUpdate) -> dict | None:
    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        cursor = conn.execute(
            """
            UPDATE catalog_items
            SET
                name = ?,
                description = ?,
                unit = ?,
                unit_price = ?,
                tax_rate = ?,
                updated_at = ?
            WHERE id = ? AND deleted_at IS NULL
            """,
            (
                payload.name,
                payload.description,
                payload.unit,
                payload.unit_price,
                payload.tax_rate,
                now,
                item_id,
            ),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None

    return get_catalog_item(database_url, item_id)


def soft_delete_catalog_item(database_url: str, item_id: str) -> bool:
    now = _utc_now()
    with closing(_connect(database_url)) as conn:
        cursor = conn.execute(
            """
            UPDATE catalog_items
            SET deleted_at = ?, updated_at = ?
            WHERE id = ? AND deleted_at IS NULL
            """,
            (now, now, item_id),
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
