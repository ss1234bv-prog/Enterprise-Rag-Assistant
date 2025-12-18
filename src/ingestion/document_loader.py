import os
from typing import List
try:
    from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
except ImportError:
    from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_core.documents import Document


class DocumentLoader:
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
    
    def __init__(self):
        pass
    
    def load_document(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext == '.docx':
            loader = Docx2txtLoader(file_path)
        elif ext == '.txt':
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        return loader.load()
    
    def load_documents(self, file_paths: List[str]) -> List[Document]:
        all_documents = []
        
        for file_path in file_paths:
            try:
                documents = self.load_document(file_path)
                all_documents.extend(documents)
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
                continue
        
        return all_documents
    
    def load_from_directory(self, directory: str) -> List[Document]:
        file_paths = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.SUPPORTED_EXTENSIONS:
                    file_paths.append(os.path.join(root, file))
        
        return self.load_documents(file_paths)
