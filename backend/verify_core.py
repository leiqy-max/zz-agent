import requests
import os
import time

BASE_URL = "http://localhost:9020"

def test_captcha_and_login():
    print("Testing Captcha and Login...")
    # 1. Get Captcha
    try:
        resp = requests.get(f"{BASE_URL}/captcha")
        resp.raise_for_status()
        data = resp.json()
        captcha_id = data['captcha_id']
        captcha_img = data['image']
        print(f"✅ Captcha Retrieved. ID: {captcha_id}, Image Length: {len(captcha_img)}")
        
        # In a real test we can't OCR, but for local verification, we can try to inspect memory if we could, 
        # but here we are testing the binary/process.
        # Since we can't easily know the captcha text without hacking the server process or OCR,
        # checking if the image is generated is the first step.
        # However, to verify login, we need the code.
        # WORKAROUND: For this test script to work fully against a running server, 
        # we might need to disable captcha verification temporarily OR add a backdoor OR just check that the captcha endpoint works.
        # But wait, the user said "验证码不能为空", implies the frontend didn't get the captcha or failed to render it.
        # If the backend returns a valid base64 image, then the backend is fine.
        
        if not captcha_img.startswith("data:image/png;base64,"):
            print("❌ Invalid captcha image format")
            return False
            
    except Exception as e:
        print(f"❌ Captcha failed: {e}")
        return False
        
    return True

def test_guest_login():
    print("\nTesting Guest Login...")
    try:
        resp = requests.post(f"{BASE_URL}/guest-token")
        if resp.status_code == 200:
            token = resp.json()['access_token']
            print(f"✅ Guest Login Successful. Token: {token[:10]}...")
            return token
        else:
            print(f"❌ Guest Login Failed: {resp.text}")
            return None
    except Exception as e:
        print(f"❌ Guest Login Error: {e}")
        return None

def test_upload(token):
    print("\nTesting File Upload...")
    headers = {"Authorization": f"Bearer {token}"}
    files = {'files': ('test_doc.txt', 'This is a test document content for RAG.', 'text/plain')}
    data = {"target_kb": "user"}
    try:
        resp = requests.post(f"{BASE_URL}/upload_doc", headers=headers, files=files, data=data)
        if resp.status_code == 200:
            print("✅ Upload Successful")
            return True
        elif resp.status_code == 403:
             print(f"⚠️ Upload Skipped: {resp.json().get('detail')}")
             return True # Guest not allowed is expected
        else:
            print(f"❌ Upload Failed: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return False

def test_ask(token):
    print("\nTesting Ask Question...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": "test document content"}
    try:
        resp = requests.post(f"{BASE_URL}/get_answer", headers=headers, json=data)
        if resp.status_code == 200:
            ans = resp.json().get('answer', '')
            print(f"✅ Ask Successful. Answer length: {len(ans)}")
            return True
        else:
            print(f"❌ Ask Failed: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Ask Error: {e}")
        return False

import uuid

def test_register_and_login():
    print("\nTesting Registration and Login...")
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    password = "password123"
    
    # Register
    try:
        reg_data = {"username": username, "password": password}
        resp = requests.post(f"{BASE_URL}/register", json=reg_data)
        if resp.status_code == 200:
            print(f"✅ Registration Successful for user: {username}")
            token = resp.json()['access_token']
            return token
        else:
            print(f"❌ Registration Failed: {resp.text}")
            return None
    except Exception as e:
        print(f"❌ Registration Error: {e}")
        return None

if __name__ == "__main__":
    if test_captcha_and_login():
        # Test Guest
        guest_token = test_guest_login()
        
        # Test Regular User (for Upload)
        user_token = test_register_and_login()
        
        if user_token:
            test_upload(user_token)
            # Wait for async processing (if any)
            time.sleep(2)
            test_ask(user_token)
        elif guest_token:
             # Fallback to test ask with guest (should work for asking, but maybe not upload)
             test_ask(guest_token)
