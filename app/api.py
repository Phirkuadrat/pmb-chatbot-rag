from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import redis
import hashlib
import json as _json
from typing import Optional
from functools import lru_cache

from app.core.config import settings
from app.models.chat import ChatRequest, ChatResponse, ChatResponseData, SourceMetadata
from app.services.rag_engine import PMBRagEngine

router = APIRouter()
from app.services.ingestion import run_ingestion

@router.get("/ingest")
async def trigger_ingestion():
    try:
        run_ingestion()
        return {"status": "Ingesti berhasil diselesaikan!"}
    except Exception as e:
        return {"status": f"Error: {e}"}


# Dependency for RAG Engine - Cached to preserve chat history (MemorySaver)
@lru_cache()
def get_engine():
    # Using lru_cache ensures PMBRagEngine and its checkpointer act as a singleton
    # across requests. Otherwise, memory is wiped clean every HTTP hit.
    return PMBRagEngine()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    engine: PMBRagEngine = Depends(get_engine)
):
    try:
        # Panggil LLM secara sinkron
        result = engine.ask(request.query, session_id=request.session_id)

        response_data = {
            "answer": result["answer"],
            "sources": result.get("detailed_sources", []),
            "retrieval_context": result.get("retrieval_context", []),
            "latency": result.get("latency", 0.0)
        }

        return ChatResponse(
            status="success",
            data=ChatResponseData(**response_data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def chat_stream_endpoint(
    request: ChatRequest,
    engine: PMBRagEngine = Depends(get_engine)
):
    async def event_generator():
        try:
            # We don't read from cache for the stream to keep it simple and real-time.
            # You could add cache logic here if needed.
            async for chunk in engine.ask_stream(request.query, request.session_id):
                yield f"data: {_json.dumps(chunk)}\n\n"
        except Exception as e:
            yield f"data: {_json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
