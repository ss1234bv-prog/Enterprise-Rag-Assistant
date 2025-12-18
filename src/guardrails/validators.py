from typing import List, Optional
from pydantic import BaseModel, Field, validator


class SourceCitation(BaseModel):
    source: str = Field(..., description="Source document name")
    page: Optional[str] = Field(None, description="Page number")
    relevance: Optional[float] = Field(None, description="Relevance score")
    chunk_id: Optional[str] = Field(None, description="Chunk identifier")
    content: Optional[str] = Field(None, description="Chunk content")


class RAGResponse(BaseModel):
    answer: str = Field(..., description="The generated answer")
    sources: List[SourceCitation] = Field(default_factory=list, description="Source citations")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    
    @validator('answer')
    def answer_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Answer cannot be empty")
        return v


class QueryValidation(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000, description="User query")
    
    @validator('query')
    def query_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


def validate_query(query: str) -> str:
    validated = QueryValidation(query=query)
    return validated.query


def create_rag_response(
    answer: str,
    sources: List[tuple] = None,
    confidence: float = None
) -> RAGResponse:
    citations = []
    
    if sources:
        for source_info in sources:
            if len(source_info) >= 2:
                citation = SourceCitation(
                    source=source_info[0],
                    page=str(source_info[1]) if source_info[1] else None,
                    relevance=source_info[2] if len(source_info) > 2 else None,
                    chunk_id=str(source_info[3]) if len(source_info) > 3 else None,
                    content=source_info[4] if len(source_info) > 4 else None
                )
                citations.append(citation)
    
    return RAGResponse(
        answer=answer,
        sources=citations,
        confidence=confidence
    )
