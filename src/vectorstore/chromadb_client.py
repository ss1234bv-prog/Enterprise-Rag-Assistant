import chromadb
from typing import List, Dict, Any, Optional


class ChromaDBClient:
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )
    
    def get_or_create_collection(self, collection_name: str) -> chromadb.Collection:
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def delete_collection(self, collection_name: str) -> None:
    
        try:
            self.client.delete_collection(name=collection_name)
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")
    
    def list_collections(self) -> List[str]:
       
        collections = self.client.list_collections()
        return [col.name for col in collections]
    
    def get_collection_count(self, collection_name: str) -> int:
       
        try:
            collection = self.client.get_collection(name=collection_name)
            return collection.count()
        except Exception:
            return 0
