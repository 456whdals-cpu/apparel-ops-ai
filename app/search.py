from time import perf_counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SEARCH_FIELDS = [
    "brand", "season", "category", "material", "color", "status",
    "storage_location", "due_date", "notes",
]


def searchable_text(item: dict) -> str:
    return " ".join(str(item.get(field, "")) for field in SEARCH_FIELDS)


def matched_fields(query: str, item: dict) -> list[str]:
    tokens = {token.lower() for token in query.split() if len(token) > 1}
    return [
        field for field in SEARCH_FIELDS
        if any(token in str(item.get(field, "")).lower() for token in tokens)
    ]


def search_items(query: str, items: list[dict], limit: int = 5) -> dict:
    started = perf_counter()
    if not items:
        return {"query": query, "total_candidates": 0, "results": [], "elapsed_ms": 0.0}
    corpus = [searchable_text(item) for item in items]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1)
    matrix = vectorizer.fit_transform(corpus + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked = scores.argsort()[::-1][:limit]
    results = [
        {
            "item": items[int(i)],
            "score": round(float(scores[i]), 4),
            "matched_fields": matched_fields(query, items[int(i)]),
        }
        for i in ranked if scores[i] > 0
    ]
    return {
        "query": query,
        "total_candidates": len(items),
        "results": results,
        "elapsed_ms": round((perf_counter() - started) * 1000, 2),
    }


