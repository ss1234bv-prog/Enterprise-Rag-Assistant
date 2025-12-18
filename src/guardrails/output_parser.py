import re
from typing import List, Tuple


class OutputParser:
    
    @staticmethod
    def extract_sources(response: str) -> List[str]:
        pattern = r'\[Source \d+: (.+?)\]'
        matches = re.findall(pattern, response)
        return matches
    
    @staticmethod
    def check_hallucination_indicators(response: str) -> bool:
        hallucination_phrases = [
            "i don't have enough information",
            "i cannot answer",
            "not mentioned in the context",
            "based on my knowledge",
            "i believe",
            "i think",
            "probably",
            "might be"
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in hallucination_phrases)
    
    @staticmethod
    def validate_response_length(response: str, min_length: int = 10) -> bool:
        return len(response.strip()) >= min_length
    
    @staticmethod
    def sanitize_response(response: str) -> str:
        response = ' '.join(response.split())
        response = response.strip('`')
        return response.strip()
