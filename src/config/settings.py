import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    
    openai_api_key: str
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.0
    openai_max_tokens: int = 1000
    
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "enterprise_documents"
    
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    top_k: int = 5
    similarity_threshold: float = 0.7
    
    upload_directory: str = "./data/documents"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
