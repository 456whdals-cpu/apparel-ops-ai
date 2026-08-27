from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    brand: str = Field(min_length=1, max_length=80, description="브랜드명", examples=["NOVA"])
    season: str = Field(min_length=1, max_length=30, description="시즌", examples=["2026 FW"])
    category: str = Field(min_length=1, max_length=50, description="품목", examples=["재킷"])
    material: str = Field(min_length=1, max_length=80, description="소재", examples=["울 혼방"])
    color: str = Field(min_length=1, max_length=40, description="색상", examples=["네이비"])
    status: str = Field(min_length=1, max_length=40, description="현재 진행 상태", examples=["검수 중"])
    storage_location: str = Field(min_length=1, max_length=80, description="샘플 보관 위치", examples=["A-01"])
    due_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="처리 납기일", examples=["2026-09-10"])
    notes: str = Field(default="", max_length=500, description="확인 사항", examples=["소매 실측 재확인 필요"])


class Item(ItemCreate):
    id: int
    created_at: str


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=200, description="기억나는 업무 단어", examples=["네이비 재킷 검수"])
    limit: int = Field(default=5, ge=1, le=20, description="최대 결과 건수")


class SearchResult(BaseModel):
    item: Item
    score: float
    matched_fields: list[str]


class SearchResponse(BaseModel):
    query: str
    total_candidates: int
    results: list[SearchResult]
    elapsed_ms: float
