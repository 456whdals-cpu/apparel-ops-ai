from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    brand: str = Field(min_length=1, max_length=80)
    season: str = Field(min_length=1, max_length=30)
    category: str = Field(min_length=1, max_length=50)
    material: str = Field(min_length=1, max_length=80)
    color: str = Field(min_length=1, max_length=40)
    status: str = Field(min_length=1, max_length=40)
    storage_location: str = Field(min_length=1, max_length=80)
    due_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    notes: str = Field(default="", max_length=500)


class Item(ItemCreate):
    id: int
    created_at: str


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=200)
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    item: Item
    score: float
    matched_fields: list[str]


class SearchResponse(BaseModel):
    query: str
    total_candidates: int
    results: list[SearchResult]
    elapsed_ms: float


