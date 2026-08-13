import requests

API_URL = "http://localhost:11434/api/chat"

def call_ollama(prompt, model):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "keep_alive": "30m"
    }
    response = requests.post(API_URL, headers=headers, json=data, timeout=300)
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        raise Exception(f"Failed to call Ollama API: {response.status_code} - {response.text}")
