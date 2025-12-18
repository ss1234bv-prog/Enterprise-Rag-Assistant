from typing import List
try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    from langchain.embeddings import OpenAIEmbeddings
from tenacity import retry, stop_after_attempt, wait_exponential


class EmbeddingGenerator:
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model=model
        )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embed_query(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
