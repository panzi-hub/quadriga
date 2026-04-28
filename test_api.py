#!/usr/bin/env python3
"""
Test script to verify API configuration from .env file.
"""
import os
from pathlib import Path
from openai import OpenAI

# Load .env file
def load_dotenv():
    """Load .env file if it exists."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print("Error: .env file not found")
        return False
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
    return True

# Test API connection
def test_api_connection():
    """Test API connection using the configured settings."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("HARNESS_MODEL", "gpt-4o")
    
    print(f"Testing API configuration:")
    print(f"  API Key: {'Set' if api_key else 'Not set'}")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model}")
    
    if not api_key:
        print("Error: API key not set")
        return False
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=30.0,
        )
        
        print("\nTesting API connection...")
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=5,
        )
        
        print(f"API response type: {type(resp)}")
        print(f"API response: {resp}")
        
        if hasattr(resp, 'choices') and resp.choices:
            print(f"API OK — model responded: {resp.choices[0].message.content}")
            return True
        else:
            print("Error: API response has no choices")
            return False
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    if load_dotenv():
        test_api_connection()
