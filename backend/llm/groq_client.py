# backend/llm/groq_client.py
import os
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.ai/v1/query"  # Endpoint placeholder

class GroqClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY não definida")

    def query(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt
        }

        try:
            response = requests.post(
                GROQ_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("text", "").strip()
        except Exception as e:
            raise RuntimeError(f"Erro na requisição à API Groq: {e}")