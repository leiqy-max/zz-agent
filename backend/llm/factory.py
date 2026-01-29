import os
from .base import BaseLLM, BaseEmbedding
from .zhipu_client import ZhipuLLM, ZhipuEmbedding
from .ollama_client import OllamaLLM, OllamaEmbedding

def get_llm_client(model: str = None) -> BaseLLM:
    provider = os.getenv("LLM_PROVIDER", "zhipu").lower()
    if provider == "ollama":
        return OllamaLLM(model=model or os.getenv("LLM_MODEL", "qwen:7b"))
    else:
        return ZhipuLLM(model=model or os.getenv("LLM_MODEL", "glm-4"))

def get_embedding_client() -> BaseEmbedding:
    provider = os.getenv("LLM_PROVIDER", "zhipu").lower()
    if provider == "ollama":
        return OllamaEmbedding(model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"))
    else:
        return ZhipuEmbedding(model=os.getenv("EMBEDDING_MODEL", "embedding-2"))
