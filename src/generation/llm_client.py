from typing import List, Dict, Any
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class LLMClient:
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.0,
        max_tokens: int = 1000
    ):
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def generate(self, prompt: str, system_message: str = None) -> str:
        messages = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessage(content=prompt))
        
        response = self.llm.invoke(messages)
        return response.content
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        system_message: str = None
    ) -> str:
        if system_message is None:
            system_message = """You are a helpful AI assistant. Answer questions based on the provided context.
If you cannot answer based on the context, say so. Always cite your sources."""
        
        prompt = f"""Context:
{context}

Question: {query}

Answer (cite sources):"""
        
        return self.generate(prompt, system_message)
