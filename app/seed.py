from datetime import date, timedelta

from app.database import connection, init_db

BRANDS = ["NOVA", "URBAN FIT", "DAILY WEAR", "ACTIVE LINE"]
CATEGORIES = ["티셔츠", "셔츠", "재킷", "팬츠", "후디"]
MATERIALS = ["면 100%", "면 폴리 혼방", "나일론", "린넨", "울 혼방"]
COLORS = ["블랙", "화이트", "네이비", "베이지", "그레이"]
STATUSES = ["요청 접수", "샘플 준비", "검수 중", "발송 완료"]
LOCATIONS = ["A-01", "A-02", "B-01", "B-02", "C-01"]


def generate_records(count: int = 120):
    base = date(2026, 8, 1)
    for i in range(count):
        yield {
            "brand": BRANDS[i % len(BRANDS)],
            "season": "2026 FW" if i % 2 == 0 else "2027 SS",
            "category": CATEGORIES[i % len(CATEGORIES)],
            "material": MATERIALS[(i * 2) % len(MATERIALS)],
            "color": COLORS[(i * 3) % len(COLORS)],
            "status": STATUSES[(i // 3) % len(STATUSES)],
            "storage_location": LOCATIONS[(i * 7) % len(LOCATIONS)],
            "due_date": str(base + timedelta(days=i % 45)),
            "notes": f"합성 샘플 데이터 {i + 1}; 실측 및 품질 기준 확인 대상",
        }


def seed(count: int = 120) -> int:
    init_db()
    inserted = 0
    with connection() as conn:
        for row in generate_records(count):
            cur = conn.execute(
                """INSERT OR IGNORE INTO items
                (brand, season, category, material, color, status, storage_location, due_date, notes)
                VALUES (:brand, :season, :category, :material, :color, :status,
                        :storage_location, :due_date, :notes)""",
                row,
            )
            inserted += cur.rowcount
    return inserted


if __name__ == "__main__":
    print({"inserted": seed()})


