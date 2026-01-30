from typing import List
from .base import BaseLLM, BaseEmbedding

class MockLLM(BaseLLM):
    def __init__(self, model: str = "mock-model"):
        self.model = model

    def chat(self, messages: List[dict], temperature: float = 0.7) -> str:
        return f"This is a mock response from {self.model}. Your last message was: {messages[-1]['content']}"

class MockEmbedding(BaseEmbedding):
    def __init__(self, model: str = "mock-embedding"):
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        # Return a fixed 1024-dim vector for testing
        return [0.1] * 1024
