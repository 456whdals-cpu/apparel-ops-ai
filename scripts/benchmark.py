from statistics import mean
from time import perf_counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.repository import all_items
from app.search import search_items
from app.seed import seed

seed()
items = all_items()
queries = ["네이비 재킷 검수", "2027 SS 면 티셔츠", "A-01 발송 완료", "울 혼방 베이지"]
latencies = []
for _ in range(25):
    for query in queries:
        started = perf_counter()
        search_items(query, items, 5)
        latencies.append((perf_counter() - started) * 1000)

latencies.sort()
print({
    "records": len(items),
    "queries": len(latencies),
    "mean_ms": round(mean(latencies), 2),
    "p95_ms": round(latencies[int(len(latencies) * 0.95) - 1], 2),
    "max_ms": round(max(latencies), 2),
})

