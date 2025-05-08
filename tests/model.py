import pytest
import requests
import os
import json

# Get the service URL from environment variable or use default for testing
SERVICE_URL = os.environ.get('SERVICE_URL')
if not SERVICE_URL:
    raise ValueError("SERVICE_URL is not set")

class TestPortkeyModel:
    def test_openai_chat_completions(self):
        response = requests.post(
            f"{SERVICE_URL}/v1/chat/completions",
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
                "x-portkey-provider": "openai"
            },
            json={
                "messages": [
                    {
                        "role": "user",
                        "content": "Just say hi"
                    }
                ],
                "max_tokens": 1000,
                "model": "gpt-4o-mini"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "choices" in data
        assert len(data["choices"]) > 0
        
    def test_embeddings(self):
        response = requests.post(
            f"{SERVICE_URL}/v1/embeddings",
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
                "x-portkey-provider": "openai"
            },
            json={
                "input": ["hello"],
                "model": "text-embedding-ada-002"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        
    def test_image_generation(self):
        response = requests.post(
            f"{SERVICE_URL}/v1/images/generations",
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
                "x-portkey-provider": "openai"
            },
            json={
                "model": "dall-e-2",
                "prompt": "a white siamese cat",
                "n": 1,
                "size": "512x512",
            }
        )
        # Handle rate limiting (429) gracefully
        if response.status_code == 429:
            return  # Skip test if rate limited
            
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert len(data["data"]) > 0, "Response data array is empty"