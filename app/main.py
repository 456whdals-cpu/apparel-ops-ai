import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from app.database import init_db
from app.repository import all_items, create_item, list_items, metrics
from app.schemas import Item, ItemCreate, SearchRequest, SearchResponse
from app.search import search_items
from app.seed import seed

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    if not all_items():
        seed()
    yield

app = FastAPI(
    title="의류 샘플 업무 검색 시스템",
    description=(
        "브랜드별 샘플의 소재·색상·진행 상태·보관 위치·납기일을 한곳에서 조회하는 API입니다. "
        "먼저 웹 업무 화면(`/`)을 사용하고, 개발자는 이 문서에서 API를 시험할 수 있습니다."
    ),
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "업무 화면", "description": "현업 담당자가 사용하는 한국어 화면"},
        {"name": "샘플 조회", "description": "샘플 목록, 조건 필터 및 통합 검색"},
        {"name": "샘플 등록", "description": "새 샘플 업무 정보 등록"},
        {"name": "운영 확인", "description": "서버 상태와 데이터 현황 확인"},
    ],
)


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", tags=["운영 확인"], summary="서버 정상 작동 확인")
def health():
    return {"status": "ok"}


@app.get(
    "/api/v1/items",
    response_model=list[Item],
    tags=["샘플 조회"],
    summary="샘플 목록 및 조건 조회",
    description="전체 샘플을 납기일 순으로 보여줍니다. 브랜드와 진행 상태를 함께 지정할 수 있습니다.",
)
def get_items(
    brand: str | None = Query(default=None, description="브랜드명 (예: NOVA)"),
    status: str | None = Query(default=None, description="진행 상태 (예: 검수 중)"),
    limit: int = Query(default=100, ge=1, le=500, description="최대 조회 건수"),
):
    return list_items(brand=brand, status=status, limit=limit)


@app.post(
    "/api/v1/items",
    response_model=Item,
    status_code=201,
    tags=["샘플 등록"],
    summary="새 샘플 등록",
    description="새로운 샘플의 기본 정보, 진행 상태, 위치와 납기를 등록합니다.",
)
def post_item(item: ItemCreate):
    try:
        return create_item(item)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="동일한 샘플 데이터가 이미 존재합니다.") from exc


@app.post(
    "/api/v1/search",
    response_model=SearchResponse,
    tags=["샘플 조회"],
    summary="업무 문장으로 샘플 검색",
    description="예: `네이비 재킷 검수`처럼 기억나는 단어를 함께 입력하면 관련 샘플부터 보여줍니다.",
)
def post_search(request: SearchRequest):
    return search_items(request.query, all_items(), request.limit)


@app.get(
    "/api/v1/metrics",
    tags=["운영 확인"],
    summary="샘플 업무 현황 요약",
    description="전체 샘플 수, 브랜드 수와 단계별 업무 건수를 반환합니다.",
)
def get_metrics():
    return metrics()
