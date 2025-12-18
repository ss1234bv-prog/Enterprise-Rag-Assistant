from langchain_core.prompts import PromptTemplate


RAG_PROMPT_TEMPLATE = """You are an expert AI assistant helping users find information from enterprise documents.

Context Information:
{context}

User Question: {question}

Instructions:
1. Answer the question based ONLY on the provided context
2. If the context doesn't contain enough information, say "I don't have enough information to answer this question."
3. Always cite the source documents in your answer
4. Be concise and precise
5. Do not make up information

Answer:"""


SYSTEM_MESSAGE = """You are a helpful AI assistant specialized in answering questions from enterprise documents.
Your responses should be:
- Accurate and grounded in the provided context
- Well-structured and easy to understand
- Include citations to source documents
- Professional and concise"""


def get_rag_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["context", "question"],
        template=RAG_PROMPT_TEMPLATE
    )


def format_rag_prompt(context: str, question: str) -> str:
    prompt = get_rag_prompt()
    return prompt.format(context=context, question=question)
