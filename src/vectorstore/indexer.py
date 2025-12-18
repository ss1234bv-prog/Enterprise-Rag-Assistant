from typing import List
import shutil
import os
from langchain_core.documents import Document
try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    from langchain.vectorstores import Chroma
try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    from langchain.embeddings import OpenAIEmbeddings


class VectorIndexer:
    
    def __init__(
        self,
        api_key: str,
        embedding_model: str = "text-embedding-3-small",
        persist_directory: str = "./chroma_db",
        collection_name: str = "enterprise_documents"
    ):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model=embedding_model
        )
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.vectorstore = None
        self.embedding_model = embedding_model
    
    def index_documents(self, documents: List[Document]) -> None:
        if not documents:
            raise ValueError("No documents to index")
        
        try:
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name
                )
            else:
                self.vectorstore.add_documents(documents)
        except Exception as e:
            if "expecting embedding with dimension" in str(e):
                print(f"Dimension mismatch detected. Recreating database with {self.embedding_model}...")
                self.delete_collection()
                if os.path.exists(self.persist_directory):
                    shutil.rmtree(self.persist_directory)
                os.makedirs(self.persist_directory, exist_ok=True)
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name
                )
            else:
                raise
    
    def load_vectorstore(self) -> Chroma:
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )
        return self.vectorstore
    
    def get_vectorstore(self) -> Chroma:
        if self.vectorstore is None:
            self.load_vectorstore()
        return self.vectorstore
    
    def delete_collection(self) -> None:
        if self.vectorstore is not None:
            self.vectorstore.delete_collection()
            self.vectorstore = None
