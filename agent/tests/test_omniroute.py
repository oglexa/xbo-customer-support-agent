"""
Test OmniRoute via OpenAI-compatible /v1/chat/completions endpoint.
OmniRoute is an OpenAI-compatible gateway, so this format should work.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
base_url = os.getenv("ANTHROPIC_BASE_URL", "http://localhost:20128")
model = os.getenv("ANTHROPIC_MODEL", "kr/claude-haiku-4.5")

print(f"Base URL: {base_url}")
print(f"Model:    {model}")
print(f"API Key:  {api_key[:10]}..." if api_key else "API Key: NOT SET")
print()

# Test 1: OpenAI-compatible /v1/chat/completions endpoint
print("=== Test 1: /v1/chat/completions (OpenAI format) ===")
try:
    resp = requests.post(
        f"{base_url}/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 64,
            "messages": [{"role": "user", "content": "Say hello in one word."}],
        },
        proxies={"http": None, "https": None},
        timeout=30,
    )
    print(f"Status: {resp.status_code}")
    print(f"Headers: {dict(resp.headers)}")
    print(f"Response: {resp.text[:1000]}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 2: Anthropic /v1/messages endpoint (for comparison)
print("=== Test 2: /v1/messages (Anthropic format) ===")
try:
    resp = requests.post(
        f"{base_url}/v1/messages",
        headers={
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": model,
            "max_tokens": 64,
            "messages": [{"role": "user", "content": "Say hello in one word."}],
        },
        proxies={"http": None, "https": None},
        timeout=30,
    )
    print(f"Status: {resp.status_code}")
    print(f"Headers: {dict(resp.headers)}")
    print(f"Response: {resp.text[:1000]}")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 3: Try root endpoint to check if OmniRoute is healthy
print("=== Test 3: Health check (GET /) ===")
try:
    resp = requests.get(
        f"{base_url}/",
        proxies={"http": None, "https": None},
        timeout=10,
    )
    print(f"Status: {resp.status_code}")
    print(f"Response length: {len(resp.text)} chars")
except Exception as e:
    print(f"Error: {e}")
