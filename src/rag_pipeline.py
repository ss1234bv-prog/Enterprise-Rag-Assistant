from typing import List
from langchain_core.documents import Document

from .config import get_settings
from .ingestion import IngestionPipeline
from .vectorstore import VectorIndexer
from .retrieval import Retriever
from .generation import LLMClient, format_rag_prompt, SYSTEM_MESSAGE
from .guardrails import validate_query, create_rag_response, OutputParser, RAGResponse


class RAGPipeline:
    
    def __init__(self, api_key: str = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.openai_api_key
        
        self.ingestion_pipeline = IngestionPipeline(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap
        )
        
        self.indexer = VectorIndexer(
            api_key=self.api_key,
            embedding_model=self.settings.openai_embedding_model,
            persist_directory=self.settings.chroma_persist_directory,
            collection_name=self.settings.chroma_collection_name
        )
        
        self.llm_client = LLMClient(
            api_key=self.api_key,
            model=self.settings.openai_model,
            temperature=self.settings.openai_temperature,
            max_tokens=self.settings.openai_max_tokens
        )
        
        self.retriever = None
        self.output_parser = OutputParser()
    
    def ingest_documents(self, file_paths: List[str]) -> int:
        chunks = self.ingestion_pipeline.process_documents(file_paths)
        self.indexer.index_documents(chunks)
        vectorstore = self.indexer.get_vectorstore()
        self.retriever = Retriever(vectorstore, top_k=self.settings.top_k)
        return len(chunks)
    
    def ingest_directory(self, directory: str) -> int:
        chunks = self.ingestion_pipeline.process_directory(directory)
        self.indexer.index_documents(chunks)
        vectorstore = self.indexer.get_vectorstore()
        self.retriever = Retriever(vectorstore, top_k=self.settings.top_k)
        return len(chunks)
    
    def load_existing_index(self) -> None:
        vectorstore = self.indexer.load_vectorstore()
        self.retriever = Retriever(vectorstore, top_k=self.settings.top_k)
    
    def query(self, question: str) -> RAGResponse:
        # Validate query
        try:
            validated_question = validate_query(question)
        except ValueError as e:
            return create_rag_response(
                answer=f"Invalid query: {str(e)}",
                sources=[],
                confidence=0.0
            )
        
        # Ensure retriever is initialized
        if self.retriever is None:
            try:
                self.load_existing_index()
            except Exception as e:
                return create_rag_response(
                    answer="No documents have been indexed yet. Please upload documents first.",
                    sources=[],
                    confidence=0.0
                )
        
        # Retrieve relevant documents
        try:
            retrieved_docs = self.retriever.retrieve_with_scores(validated_question)
        except Exception as e:
            return create_rag_response(
                answer=f"Error retrieving documents: {str(e)}",
                sources=[],
                confidence=0.0
            )
        
        if not retrieved_docs:
            return create_rag_response(
                answer="No relevant documents found for your query.",
                sources=[],
                confidence=0.0
            )
        
        similarity_threshold = self.settings.similarity_threshold
        filtered_docs = []
        for doc, score in retrieved_docs:
            similarity = max(0.0, 1.0 - float(score))
            if similarity >= similarity_threshold:
                filtered_docs.append((doc, score, similarity))
        
        if not filtered_docs:
            return create_rag_response(
                answer="No relevant documents found for your query. The retrieved content does not match your question well enough.",
                sources=[],
                confidence=0.0
            )
        
        docs_only = [doc for doc, _, _ in filtered_docs]
        context = self.retriever.format_retrieved_context(docs_only)
        
        # Generate response
        prompt = format_rag_prompt(context, validated_question)
        try:
            answer = self.llm_client.generate(prompt, SYSTEM_MESSAGE)
        except Exception as e:
            return create_rag_response(
                answer=f"Error generating response: {str(e)}",
                sources=[],
                confidence=0.0
            )
        
        # Sanitize response
        answer = self.output_parser.sanitize_response(answer)
        
        sources = []
        for doc, score, similarity in filtered_docs:
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'N/A')
            chunk_id = doc.metadata.get('chunk_id', 'N/A')
            content = doc.page_content
            sources.append((source, page, similarity, chunk_id, content))
        
        avg_similarity = sum(sim for _, _, sim in filtered_docs) / len(filtered_docs)
        confidence = max(0.0, min(1.0, avg_similarity))
        
        return create_rag_response(
            answer=answer,
            sources=sources,
            confidence=confidence
        )
    
    def get_collection_stats(self) -> dict:
        try:
            vectorstore = self.indexer.get_vectorstore()
            collection = vectorstore._collection
            count = collection.count()
            
            return {
                "total_chunks": count,
                "collection_name": self.settings.chroma_collection_name,
                "chunk_size": self.settings.chunk_size,
                "chunk_overlap": self.settings.chunk_overlap
            }
        except Exception as e:
            return {
                "error": str(e),
                "total_chunks": 0
            }
