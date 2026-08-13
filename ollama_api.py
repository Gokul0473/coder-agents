import requests

API_URL = "http://localhost:11434/api/chat"

def call_ollama(prompt, model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # Replace with your actual API key
    }
    data = {
        "prompt": prompt,
        "model": model
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to call Ollama API: {response.status_code} - {response.text}")
