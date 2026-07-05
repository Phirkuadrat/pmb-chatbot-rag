from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # === LLM API Keys ===
    groq_api_key: str
    gemini_api_key: str = ""
    openrouter_api_key: str = ""
    openrouter_eval_api_key: str = ""

    # === LLM Configuration ===
    # qwen/qwen3-32b
    # meta-llama/llama-3.3-70b-instruct
    # qwen/qwen3-next-80b-a3b-instruct:free
    # google/gemma-4-31b-it
    llm_model_name: str = "qwen/qwen3-32b"
    eval_llm_model_name: str = "openai/gpt-4o-mini"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 800 
    
    # === Vector Store ===
    vector_db_path: str = "./data/chromadb"
    chroma_collection_name: str = "pmb_itenas"
    rerank_threshold: float = 0.01

    # === Data Directories ===
    raw_pdf_dir: str = "./data/raw/"
    json_data_dir: str = "./data/structured/"

    # === Redis Cache ===
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_cache_ttl: int = 3600  # seconds (1 jam)

    # === Database ===
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "pmb_itenas"

    # === Security / CORS ===
    allowed_origins: list[str] = [
        "*"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  


# Singleton instance yang digunakan di seluruh aplikasi
settings = Settings()
