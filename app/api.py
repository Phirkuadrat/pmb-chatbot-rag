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


# Dependency for Redis Cache
def get_redis():
    # Attempt to connect to local Redis. If not available, we can fallback gracefully.
    try:
        r = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
            socket_timeout=1
        )
        r.ping()
        return r
    except Exception:
        return None


def generate_cache_key(query: str, session_id: str) -> str:
    unique_str = f"{session_id}:{query.lower().strip()}"
    return "pmb_chat:" + hashlib.md5(unique_str.encode()).hexdigest()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    engine: PMBRagEngine = Depends(get_engine),
    cache: Optional[redis.Redis] = Depends(get_redis)
):
    try:
        cache_key = generate_cache_key(request.query, request.session_id)

        # 1. Check Cache
        if cache:
            cached_data = cache.get(cache_key)
            if cached_data:
                data_dict = _json.loads(cached_data)
                return ChatResponse(
                    status="success",
                    data=ChatResponseData(**data_dict)
                )

        # 2. If not cached, call LLM
        result = engine.ask(request.query, session_id=request.session_id)

        response_data = {
            "answer": result["answer"],
            "sources": result.get("detailed_sources", []),
            "retrieval_context": result.get("retrieval_context", []),
            "latency": result.get("latency", 0.0)
        }

        # 3. Save to Cache (TTL dari settings)
        if cache:
            cache.setex(cache_key, settings.redis_cache_ttl, _json.dumps(response_data))

        return ChatResponse(
            status="success",
            data=ChatResponseData(**response_data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def chat_stream_endpoint(
    request: ChatRequest,
    engine: PMBRagEngine = Depends(get_engine),
    cache: Optional[redis.Redis] = Depends(get_redis)
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
