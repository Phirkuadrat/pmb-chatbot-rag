import os
import json
import re
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder
from app.core.config import settings
from app.utils.logger import log_tool_call

VECTOR_DB_DIR = settings.vector_db_path
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Instantiate Globally to avoid loading model every time (Caching)
_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
_vector_store = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=_embeddings)
_cross_encoder = CrossEncoder("cross-encoder/mmarco-mMiniLMv2-L12-H384-v1")


def rewrite_query(query: str) -> str:
    """Pre-processing keyword ekspansi sederhana untuk meningkatkan relevansi semantic search"""
    q = query.lower()
    replacements = {
        r"\bif\b": "informatika",
        r"\bsi\b": "sistem informasi",
        r"\bti\b": "teknik industri",
        r"\bdkv\b": "desain komunikasi visual",
        r"\bpwk\b": "perencanaan wilayah dan kota",
        r"\bsnbt\b": "utbk snbt",
        r"\bodt\b": "one day test",
        r"\bgeomatika\b": "teknik geodesi geomatika",
    }
    for pattern, replacement in replacements.items():
        q = re.sub(pattern, replacement, q)
    return q


@tool
def search_knowledge_base(query: str) -> str:
    """Useful for searching ANY unstructured information from the campus knowledge base, such as academic rules, graduation requirements, schedules, scholarship info, registration periods, etc.
    Args:
        query: The search query to look up in the vector database (PDF documents).
    Returns:
        JSON string containing relevant paragraphs and source metadata.
    """

    # Normalisasi Query
    expanded_query = rewrite_query(query)

    # Semantic Retrieval
    retriever = _vector_store.as_retriever(search_kwargs={"k": 50})
    base_docs = retriever.invoke(expanded_query)

    if not base_docs:
        log_tool_call(
            "search_knowledge_base", {"query": query}, "miss", "Base retrieval kosong"
        )
        return json.dumps(
            {
                "content": "Tidak ditemukan informasi terkait aturan akademik tersebut di database dokumen.",
                "metadata": [],
            }
        )

    try:
        # Cross Encoder Re-ranking
        pairs = [[expanded_query, doc.page_content] for doc in base_docs]
        scores = _cross_encoder.predict(pairs)

        scored_docs = list(zip(base_docs, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        # Threshold Filtering
        threshold = settings.rerank_threshold
        filtered_docs = [doc for doc, score in scored_docs if score > threshold]

        if not filtered_docs:
            log_tool_call(
                "search_knowledge_base",
                {"query": query},
                "miss",
                f"Tidak ada doc melampaui threshold {threshold}",
            )
            return json.dumps(
                {
                    "content": "Maaf, sistem tidak menemukan data yang cukup relevan di knowledge base. Mohon ulangi dengan kata kunci yang lebih spesifik.",
                    "metadata": [],
                }
            )

        top_docs = filtered_docs[:10]

    except Exception as e:
        log_tool_call(
            "search_knowledge_base",
            {"query": query},
            "error",
            f"Re-ranking failed: {e}",
        )
        top_docs = base_docs[:10]

    # Collect Content and Metadata
    combined_content = "\n\n".join([doc.page_content for doc in top_docs])
    metadata_list = []

    for doc in top_docs:
        # ChromaDB stores source path inside metadata['source'] and page num in metadata['page']
        doc_meta = doc.metadata
        filename = os.path.basename(doc_meta.get("source", "unknown_document.pdf"))

        meta = {"document": filename, "type": "unstructured (PDF)"}

        if "page" in doc_meta:
            meta["page"] = doc_meta["page"]

        metadata_list.append(meta)

    log_tool_call(
        "search_knowledge_base",
        {"query": query},
        "hit",
        f"Returned {len(top_docs)} docs",
    )
    return json.dumps({"content": combined_content, "metadata": metadata_list})
