from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # === LLM API Keys ===
    groq_api_key: str
    gemini_api_key: str = ""

    # === LLM Configuration ===
    llm_model_name: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1024

    # === Vector Store ===
    vector_db_path: str = "./data/chromadb"
    chroma_collection_name: str = "pmb_itenas"

    # === Data Directories ===
    raw_pdf_dir: str = "./data/raw/"
    json_data_dir: str = "./data/structured/"

    # === Redis Cache ===
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_cache_ttl: int = 3600  # seconds (1 jam)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Abaikan variabel .env yang tidak terdaftar di sini


# Singleton instance yang digunakan di seluruh aplikasi
settings = Settings()
