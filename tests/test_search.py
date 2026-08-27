from app.search import search_items


def test_search_ranks_matching_item_first():
    items = [
        {"id": 1, "brand": "NOVA", "season": "2026 FW", "category": "재킷", "material": "울", "color": "네이비", "status": "검수 중", "storage_location": "A-01", "due_date": "2026-08-10", "notes": "실측 확인", "created_at": "now"},
        {"id": 2, "brand": "DAILY", "season": "2027 SS", "category": "티셔츠", "material": "면", "color": "화이트", "status": "발송 완료", "storage_location": "B-01", "due_date": "2026-08-11", "notes": "완료", "created_at": "now"},
    ]
    result = search_items("네이비 재킷 검수", items, 2)
    assert result["results"][0]["item"]["id"] == 1
    assert result["results"][0]["score"] > 0


def test_empty_search_dataset():
    result = search_items("검색", [], 5)
    assert result["results"] == []
    assert result["total_candidates"] == 0


