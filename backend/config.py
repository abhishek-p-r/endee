"""Configuration management for the Endee AI Knowledge Assistant."""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Endee Vector Database
    endee_url: str = os.getenv("ENDEE_URL", "http://localhost:8080")
    endee_collection_name: str = "knowledge-base"
    
    # Gemini AI
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # RAG Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    max_retrieved_documents: int = 5
    similarity_threshold: float = 0.3
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
