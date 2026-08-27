import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "app.db"


@contextmanager
def connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                season TEXT NOT NULL,
                category TEXT NOT NULL,
                material TEXT NOT NULL,
                color TEXT NOT NULL,
                status TEXT NOT NULL,
                storage_location TEXT NOT NULL,
                due_date TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(brand, season, category, material, color, due_date)
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_items_brand ON items(brand)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_items_due_date ON items(due_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_items_status ON items(status)")


