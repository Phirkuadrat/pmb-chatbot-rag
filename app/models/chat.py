from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Schema untuk request dari client ke endpoint /chat."""
    query: str
    session_id: str = "default_session"


class SourceMetadata(BaseModel):
    """Schema untuk satu sumber dokumen yang digunakan RAG."""
    document: str
    type: str
    page: Optional[int] = None
    row: Optional[int] = None


class ChatResponseData(BaseModel):
    """Schema untuk isi data pada response chat."""
    answer: str
    sources: list[SourceMetadata]
    retrieval_context: list[str] = []  # Teks chunk asli dari dokumen, untuk DeepEval
    latency: float


class ChatResponse(BaseModel):
    """Schema untuk response utama endpoint /chat."""
    status: str
    data: ChatResponseData
