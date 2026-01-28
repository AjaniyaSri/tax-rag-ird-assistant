from pydantic import BaseModel, Field
from typing import List, Optional


class Citation(BaseModel):
    document: str
    page: int
    section: str = "N/A"
    snippet: Optional[str] = None


class UploadResponse(BaseModel):
    filename: str
    saved_path: str


class IndexResponse(BaseModel):
    indexed_files: List[str]
    total_chunks: int


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=6, ge=1, le=12)


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    disclaimer: str
