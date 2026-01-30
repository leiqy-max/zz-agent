import os
import sys
import yaml
import requests
import json

def load_config():
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def test_connection():
    config = load_config()
    llm_config = config.get("llm", {})
    
    print("\n=== Testing LLM Connection (Requests - Robust) ===")
    
    provider = llm_config.get("provider", "unknown")
    api_key = llm_config.get("api_key", "dummy")
    
    # Get base_url for chat and embedding
    chat_base_url = llm_config.get("chat_base_url") or llm_config.get("base_url")
    embedding_base_url = llm_config.get("embedding_base_url") or llm_config.get("base_url")
    
    model = llm_config.get("model")
    embedding_model = llm_config.get("embedding_model")
    
    print(f"Provider: {provider}")
    print(f"Chat Base URL: {chat_base_url}")
    print(f"Embedding Base URL: {embedding_base_url}")
    print(f"Chat Model: {model}")
    print(f"Embedding Model: {embedding_model}")

    if not chat_base_url:
        print("❌ Error: base_url (or chat_base_url) is missing in config.yaml")
        return

    # Helper function to fix URL
    def fix_url(url):
        if not url: return url
        if url.endswith("/embeddings"):
            url = url.replace("/embeddings", "")
        elif url.endswith("/chat/completions"):
            url = url.replace("/chat/completions", "")
        if url.endswith("/"):
            url = url[:-1]
        return url

    fixed_chat_url = fix_url(chat_base_url)
    fixed_embedding_url = fix_url(embedding_base_url)
        
    print(f"Fixed Chat URL: {fixed_chat_url}")
    print(f"Fixed Embedding URL: {fixed_embedding_url}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 1. Test Embedding
    if embedding_model and fixed_embedding_url:
        print(f"\n[Testing Embedding: {embedding_model}]")
        url = f"{fixed_embedding_url}/embeddings"
        payload = {
            "model": embedding_model,
            "input": "hello"
        }
        try:
            print(f"POST {url}")
            print(f"Payload: {json.dumps(payload)}")
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"Response keys: {list(data.keys())}")
                if "data" in data:
                    print(f"Data type: {type(data['data'])}")
                    # Match the logic in openai_client.py
                    items = data["data"]
                    vec = None
                    
                    if isinstance(items, list) and len(items) > 0:
                        vec = items[0]["embedding"]
                    elif isinstance(items, dict):
                        if 0 in items: vec = items[0]["embedding"]
                        elif "0" in items: vec = items["0"]["embedding"]
                        elif "embedding" in items: vec = items["embedding"]
                        elif items:
                            first_val = list(items.values())[0]
                            if isinstance(first_val, dict) and "embedding" in first_val:
                                vec = first_val["embedding"]
                    
                    if vec:
                        print(f"✅ Embedding Success! Vector length: {len(vec)}")
                    else:
                        print(f"❌ Failed to extract vector. Data: {str(items)[:200]}")
                else:
                    print(f"❌ Unexpected format (no 'data'): {data}")
            else:
                print(f"❌ Failed: {resp.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
    else:
        print("\n[Skipping Embedding Test: No embedding_model configured]")

    # 2. Test Chat
    if model:
        print(f"\n[Testing Chat: {model}]")
        
        # Define candidate URLs
        candidate_urls = [f"{fixed_chat_url}/chat/completions"]
        if fixed_chat_url.endswith("/v1"):
            base_no_v1 = fixed_chat_url[:-3]
            candidate_urls.append(f"{base_no_v1}/chat/completions")
        candidate_urls.append(f"{fixed_chat_url}/chat")
        if fixed_chat_url.endswith("/v1"):
             base_no_v1 = fixed_chat_url[:-3]
             candidate_urls.append(f"{base_no_v1}/chat")

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7
        }
        
        success = False
        for url in candidate_urls:
            print(f"Trying URL: {url}")
            try:
                print(f"POST {url}")
                print(f"Payload: {json.dumps(payload)}")
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                print(f"Status Code: {resp.status_code}")
                
                if resp.status_code == 404:
                    print("❌ 404 Not Found - Trying next...")
                    continue
                
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"✅ Chat Success! Response: {data['choices'][0]['message']['content']}")
                    success = True
                    break
                else:
                    print(f"❌ Failed: {resp.text}")
                    # Don't try next if it's not 404 (e.g. 500 or 400)
                    break
            except Exception as e:
                print(f"❌ Exception: {e}")
                # Stop on connection errors
                break
        
        if not success:
            print("❌ All Chat URLs failed.")
    else:
        print("\n[Skipping Chat Test: No model configured]")

if __name__ == "__main__":
    test_connection()
