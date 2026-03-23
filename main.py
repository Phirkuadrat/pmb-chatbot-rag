from fastapi import FastAPI
from app.api import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure basic logging for Production visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Chatbot PMB Itenas API",
    description="Backend RAG menggunakan Llama 3.3 70B, JSON, dan ChromaDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
async def root():
    logger.info("Root healthcheck endpoint called")
    return {
        "message": "Server Chatbot PMB Itenas aktif!",
        "docs": "/docs"
    }

