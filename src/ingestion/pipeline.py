from typing import List
from langchain_core.documents import Document
from .document_loader import DocumentLoader
from .text_splitter import TextSplitter


class IngestionPipeline:
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.loader = DocumentLoader()
        self.splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    def process_documents(self, file_paths: List[str]) -> List[Document]:
        documents = self.loader.load_documents(file_paths)
        
        for doc in documents:
            doc.page_content = self.splitter.preprocess_text(doc.page_content)
        
        chunks = self.splitter.split_documents(documents)
        return chunks
    
    def process_directory(self, directory: str) -> List[Document]:
        documents = self.loader.load_from_directory(directory)
        
        for doc in documents:
            doc.page_content = self.splitter.preprocess_text(doc.page_content)
        
        chunks = self.splitter.split_documents(documents)
        return chunks
