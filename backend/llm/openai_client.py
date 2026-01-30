import os
import requests
import json
from typing import List, Dict, Any, Union
from .base import BaseLLM, BaseEmbedding
from config_loader import config

class OpenAILLM(BaseLLM):
    def __init__(self, api_key: str = None, model: str = None):
        llm_config = config.llm
        self.api_key = api_key or llm_config.get("api_key") or "dummy"
        # Prioritize chat_base_url, then base_url
        self.base_url = llm_config.get("chat_base_url") or llm_config.get("base_url") or os.getenv("OPENAI_BASE_URL") or "http://localhost:8000/v1"
        self.model = model or llm_config.get("model") or "gpt-3.5-turbo"

        # Fix base_url
        if self.base_url.endswith("/embeddings"):
            self.base_url = self.base_url.replace("/embeddings", "")
        elif self.base_url.endswith("/chat/completions"):
            self.base_url = self.base_url.replace("/chat/completions", "")
        
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]
        
        print(f"Initializing OpenAI LLM (Requests) with base_url={self.base_url}, model={self.model}")

    def chat(self, messages: List[dict], temperature: float = 0.7) -> str:
        # Define candidate URLs
        candidate_urls = [f"{self.base_url}/chat/completions"]
        
        # If base_url ends with /v1, try without it
        if self.base_url.endswith("/v1"):
            base_no_v1 = self.base_url[:-3]
            candidate_urls.append(f"{base_no_v1}/chat/completions")
            
        # Try /v1/chat (some custom servers)
        candidate_urls.append(f"{self.base_url}/chat")
        
        # Try /chat (without v1)
        if self.base_url.endswith("/v1"):
             base_no_v1 = self.base_url[:-3]
             candidate_urls.append(f"{base_no_v1}/chat")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        last_error = None
        
        for url in candidate_urls:
            try:
                print(f"DEBUG: Trying Chat URL: {url}")
                response = requests.post(url, headers=headers, json=payload, timeout=60)
                
                if response.status_code == 404:
                    print(f"DEBUG: 404 Not Found at {url}")
                    last_error = f"404 Not Found at {url}"
                    continue # Try next URL
                
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except Exception as e:
                # If exception is raised by raise_for_status() other than 404 (e.g. 500, 400), we stop.
                # If it's a connection error, we might want to fail too unless we want to try other URLs for connection issues?
                # Assume 404 is the main reason to switch URLs.
                last_error = str(e)
                if 'response' in locals() and response.status_code != 404:
                     error_msg = f"Error calling OpenAI Chat API ({url}): {last_error} Response: {response.text}"
                     print(error_msg)
                     return f"Error: {error_msg}"
                elif not 'response' in locals():
                     # Connection error
                     print(f"Connection error calling {url}: {last_error}")
                     # Maybe try next URL if it's a connection error? 
                     # No, connection error usually means host is wrong or down, not path is wrong.
                     return f"Error: Connection error: {last_error}"

        # If we exhausted all URLs
        return f"Error: Could not find valid chat endpoint. Tried: {candidate_urls}. Last error: {last_error}"

class OpenAIEmbedding(BaseEmbedding):
    def __init__(self, api_key: str = None, model: str = None):
        llm_config = config.llm
        self.api_key = api_key or llm_config.get("api_key") or "dummy"
        # Prioritize embedding_base_url, then base_url
        self.base_url = llm_config.get("embedding_base_url") or llm_config.get("base_url") or os.getenv("OPENAI_BASE_URL") or "http://localhost:8000/v1"
        # Note: config.llm.get("model") might be the chat model, check embedding_model first
        self.model = model or llm_config.get("embedding_model") or llm_config.get("model") or "text-embedding-ada-002"

        # Fix base_url
        if self.base_url.endswith("/embeddings"):
            self.base_url = self.base_url.replace("/embeddings", "")
        elif self.base_url.endswith("/chat/completions"):
            self.base_url = self.base_url.replace("/chat/completions", "")
        
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]

        print(f"Initializing OpenAI Embedding (Requests) with base_url={self.base_url}, model={self.model}")

    def embed_text(self, text: str) -> List[float]:
        url = f"{self.base_url}/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "input": text
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Robust extraction logic to handle various response formats
            if "data" in data:
                items = data["data"]
                
                # Case 1: Standard OpenAI List
                if isinstance(items, list):
                    if len(items) > 0:
                        return items[0]["embedding"]
                
                # Case 2: Dictionary mimicking list or direct object
                elif isinstance(items, dict):
                    # Try integer index 0
                    if 0 in items:
                        return items[0]["embedding"]
                    # Try string index "0"
                    if "0" in items:
                        return items["0"]["embedding"]
                    # Try direct embedding field (if data is the item itself)
                    if "embedding" in items:
                        return items["embedding"]
                    # Try first value if it's a dict of items
                    if items:
                        first_val = list(items.values())[0]
                        if isinstance(first_val, dict) and "embedding" in first_val:
                            return first_val["embedding"]
            
            # Debugging info if we fail
            debug_info = {
                "keys": list(data.keys()),
                "data_type": str(type(data.get("data"))),
                "data_sample": str(data.get("data"))[:200]
            }
            raise ValueError(f"Unexpected response format. Debug: {debug_info}")

        except Exception as e:
            error_msg = f"Error calling OpenAI Embedding API ({url}): {str(e)}"
            if 'response' in locals():
                error_msg += f" Response: {response.text}"
            print(error_msg)
            raise e
