import os
from .base import BaseLLM, BaseEmbedding
from .zhipu_client import ZhipuLLM, ZhipuEmbedding
from .ollama_client import OllamaLLM, OllamaEmbedding
from .mock_client import MockLLM, MockEmbedding
from .openai_client import OpenAILLM, OpenAIEmbedding
from config_loader import config

def get_llm_client(model: str = None) -> BaseLLM:
    provider = config.llm.get("provider") or os.getenv("LLM_PROVIDER", "zhipu")
    provider = provider.lower()
    
    if provider == "ollama":
        return OllamaLLM(model=model or os.getenv("LLM_MODEL", "qwen:7b"))
    elif provider == "mock":
        return MockLLM(model=model or "mock-gpt")
    elif provider in ["openai", "deepseek", "deepseek-v3", "local", "vllm"]:
        return OpenAILLM(model=model)
    else:
        # Pass None to let the client class handle defaults/config
        return ZhipuLLM(model=model)

def get_embedding_client() -> BaseEmbedding:
    provider = config.llm.get("provider") or os.getenv("LLM_PROVIDER", "zhipu")
    provider = provider.lower()
    
    if provider == "ollama":
        return OllamaEmbedding(model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"))
    elif provider == "mock":
        return MockEmbedding(model="mock-embedding")
    elif provider in ["openai", "deepseek", "deepseek-v3", "local", "vllm"]:
        return OpenAIEmbedding(model=None)
    else:
        # Pass None to let the client class handle defaults/config
        return ZhipuEmbedding(model=None)
