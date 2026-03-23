import os
import json
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv

load_dotenv()
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./data/chromadb")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

@tool
def search_knowledge_base(query: str) -> str:
    """Useful for searching ANY unstructured information from the campus knowledge base, such as academic rules, graduation requirements, schedules, scholarship info, registration periods, etc.
    Args:
        query: The search query to look up in the vector database (PDF documents).
    Returns:
        JSON string containing relevant paragraphs and source metadata.
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )
    
    # 1. Base Retrieval (Get top 10 as candidates)
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    base_docs = retriever.invoke(query)
    
    if not base_docs:
        return json.dumps({"content": "Tidak ditemukan informasi terkait aturan akademik tersebut di database dokumen.", "metadata": []})
        
    # 2. Re-Ranking (CrossEncoder)
    try:
        # Pake model ringan bahasa Indonesia/Multibahasa untuk reranking
        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 
        
        # Format pasangan [query, document_text]
        pairs = [[query, doc.page_content] for doc in base_docs]
        scores = cross_encoder.predict(pairs)
        
        # Gabungkan doc dengan score-nya
        scored_docs = list(zip(base_docs, scores))
        # Sort dari yang score tertinggi
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # 3. Filter and take Top 3 paling relevan
        top_docs = [doc for doc, score in scored_docs[:3] if score > 0] # Asumsi threshold dasar
        
        if not top_docs:
            # Fallback kalau reranker nge-drop semua (terlalu strict)
            top_docs = base_docs[:3]
            
    except Exception as e:
        print(f"⚠️ Re-ranking failed (using base docs): {e}")
        top_docs = base_docs[:3]
        
    # Collect Content and Metadata
    combined_content = "\n\n".join([doc.page_content for doc in top_docs])
    metadata_list = []
    
    for doc in top_docs:
        # ChromaDB stores source path inside metadata['source'] and page num in metadata['page']
        doc_meta = doc.metadata
        filename = os.path.basename(doc_meta.get('source', 'unknown_document.pdf'))
        
        meta = {
            "document": filename,
            "type": "unstructured (PDF)"
        }
        
        # Add Page if available
        if 'page' in doc_meta:
            meta["page"] = doc_meta["page"]
            
        metadata_list.append(meta)
    
    return json.dumps({
        "content": combined_content,
        "metadata": metadata_list
    })
