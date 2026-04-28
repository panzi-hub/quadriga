#!/usr/bin/env python3
"""
Test script to check API connection.
"""
import os
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key:
            os.environ[key] = value

# Import after loading env
from openai import OpenAI

# Get API config
api_key = os.environ.get("OPENAI_API_KEY", "")
base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
model = os.environ.get("HARNESS_MODEL", "gpt-4o")

print(f"Testing API connection with:")
print(f"  API Key: {'Set' if api_key else 'Not set'}")
print(f"  Base URL: {base_url}")
print(f"  Model: {model}")
print()

if not api_key:
    print("Error: OPENAI_API_KEY is not set")
    exit(1)

# Test connection
try:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=30.0,
    )
    
    print("Testing API connection...")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say OK"}],
        max_tokens=5,
    )
    
    # Check response structure
    if hasattr(resp, 'choices') and len(resp.choices) > 0 and hasattr(resp.choices[0], 'message') and hasattr(resp.choices[0].message, 'content'):
        print(f"✅ API connection successful!")
        print(f"   Model responded: {resp.choices[0].message.content}")
    else:
        print(f"❌ API connection failed: Invalid response structure")
        print(f"   Response: {resp}")
        
except Exception as e:
    print(f"❌ API connection failed: {e}")
