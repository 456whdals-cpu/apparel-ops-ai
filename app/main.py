import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query

from app.database import init_db
from app.repository import all_items, create_item, list_items, metrics
from app.schemas import Item, ItemCreate, SearchRequest, SearchResponse
from app.search import search_items
from app.seed import seed


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    if not all_items():
        seed()
    yield

app = FastAPI(
    title="Apparel Operations AI Search API",
    description="의류 샘플·원단 자료를 구조화하고 TF-IDF로 검색하는 포트폴리오 API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/items", response_model=list[Item])
def get_items(
    brand: str | None = None,
    status: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
):
    return list_items(brand=brand, status=status, limit=limit)


@app.post("/api/v1/items", response_model=Item, status_code=201)
def post_item(item: ItemCreate):
    try:
        return create_item(item)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="동일한 샘플 데이터가 이미 존재합니다.") from exc


@app.post("/api/v1/search", response_model=SearchResponse)
def post_search(request: SearchRequest):
    return search_items(request.query, all_items(), request.limit)


@app.get("/api/v1/metrics")
def get_metrics():
    return metrics()

