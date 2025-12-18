from typing import List, Dict, Any
from langchain_core.documents import Document
try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    from langchain.vectorstores import Chroma


class Retriever:
    
    def __init__(self, vectorstore: Chroma, top_k: int = 5):
        self.vectorstore = vectorstore
        self.top_k = top_k
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k}
        )
    
    def retrieve(self, query: str) -> List[Document]:
        return self.retriever.get_relevant_documents(query)
    
    def retrieve_with_scores(self, query: str) -> List[tuple[Document, float]]:
        return self.vectorstore.similarity_search_with_score(query, k=self.top_k)
    
    def format_retrieved_context(self, documents: List[Document]) -> str:
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'N/A')
            chunk_id = doc.metadata.get('chunk_id', 'N/A')
            
            context_parts.append(
                f"[Source {i}: {source}, Page {page}, Chunk {chunk_id}]\n{doc.page_content}\n"
            )
        
        return "\n".join(context_parts)
