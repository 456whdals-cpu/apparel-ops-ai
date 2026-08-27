from app.database import connection
from app.schemas import ItemCreate


def row_to_dict(row):
    return dict(row) if row else None


def create_item(item: ItemCreate) -> dict:
    values = item.model_dump()
    with connection() as conn:
        cur = conn.execute(
            """INSERT INTO items
            (brand, season, category, material, color, status, storage_location, due_date, notes)
            VALUES (:brand, :season, :category, :material, :color, :status,
                    :storage_location, :due_date, :notes)""",
            values,
        )
        row = conn.execute("SELECT * FROM items WHERE id = ?", (cur.lastrowid,)).fetchone()
    return row_to_dict(row)


def list_items(brand=None, status=None, limit=100) -> list[dict]:
    clauses, params = [], []
    if brand:
        clauses.append("brand = ?")
        params.append(brand)
    if status:
        clauses.append("status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    params.append(limit)
    with connection() as conn:
        rows = conn.execute(
            f"SELECT * FROM items{where} ORDER BY due_date, id LIMIT ?", params
        ).fetchall()
    return [row_to_dict(r) for r in rows]


def all_items() -> list[dict]:
    with connection() as conn:
        rows = conn.execute("SELECT * FROM items ORDER BY id").fetchall()
    return [row_to_dict(r) for r in rows]


def metrics() -> dict:
    with connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        brands = conn.execute("SELECT COUNT(DISTINCT brand) FROM items").fetchone()[0]
        statuses = [dict(r) for r in conn.execute(
            "SELECT status, COUNT(*) count FROM items GROUP BY status ORDER BY count DESC"
        ).fetchall()]
    return {"total_items": total, "distinct_brands": brands, "status_counts": statuses}


