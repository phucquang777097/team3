import sqlite3
import os
import datetime
from typing import Optional, Dict, Any, List

from .config import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    recovery_email TEXT,
    proxy_used TEXT,
    user_agent TEXT,
    status TEXT DEFAULT 'new',
    creation_date TEXT,
    last_activity TEXT
);
"""


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def insert_account(provider: str, email: str, password: str, recovery_email: Optional[str], proxy_used: Optional[str], user_agent: Optional[str], status: str = "new") -> int:
    now = datetime.datetime.utcnow().isoformat()
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO accounts(provider, email, password, recovery_email, proxy_used, user_agent, status, creation_date, last_activity)
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (provider, email, password, recovery_email, proxy_used, user_agent, status, now, now),
        )
        conn.commit()
        return cur.lastrowid


def update_status(email: str, status: str) -> None:
    with _connect() as conn:
        conn.execute("UPDATE accounts SET status=?, last_activity=? WHERE email=?", (status, datetime.datetime.utcnow().isoformat(), email))
        conn.commit()


def list_accounts(limit: int = 50, provider: Optional[str] = None) -> List[Dict[str, Any]]:
    with _connect() as conn:
        if provider:
            rows = conn.execute("SELECT provider, email, password, status, proxy_used, last_activity FROM accounts WHERE provider=? ORDER BY id DESC LIMIT ?", (provider, limit)).fetchall()
        else:
            rows = conn.execute("SELECT provider, email, password, status, proxy_used, last_activity FROM accounts ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [
        {
            "provider": r[0],
            "email": r[1],
            "password": r[2],
            "status": r[3],
            "proxy_used": r[4],
            "last_activity": r[5],
        }
        for r in rows
    ]




