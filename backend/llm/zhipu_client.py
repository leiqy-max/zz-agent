import os
from typing import List
from zhipuai import ZhipuAI
from .base import BaseLLM, BaseEmbedding
from config_loader import config

class ZhipuLLM(BaseLLM):
    def __init__(self, api_key: str = None, model: str = None):
        llm_config = config.llm
        self.api_key = api_key or llm_config.get("api_key") or os.getenv("ZHIPUAI_API_KEY") or "dummy"
        self.base_url = llm_config.get("base_url") or os.getenv("ZHIPUAI_BASE_URL")
        
        # If using internal LLM, api_key might be optional or dummy, but SDK might require it.
        
        if self.base_url:
            self.client = ZhipuAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = ZhipuAI(api_key=self.api_key)
            
        self.model = model or llm_config.get("model") or "glm-4"

    def chat(self, messages: List[dict], temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling ZhipuAI: {str(e)}"

class ZhipuEmbedding(BaseEmbedding):
    def __init__(self, api_key: str = None, model: str = None):
        llm_config = config.llm
        self.api_key = api_key or llm_config.get("api_key") or os.getenv("ZHIPUAI_API_KEY") or "dummy"
        self.base_url = llm_config.get("base_url") or os.getenv("ZHIPUAI_BASE_URL")
        
        if self.base_url:
            self.client = ZhipuAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = ZhipuAI(api_key=self.api_key)
            
        self.model = model or llm_config.get("embedding_model") or "embedding-2"

    def embed_text(self, text: str) -> List[float]:
        resp = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return resp.data[0].embedding
