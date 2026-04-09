
# backend/llm/groq_llm.py
from backend.llm.groq_client import client
import json

def analyze_groq(content, content_type: str):
    """
    Envia conteúdo ao Groq.
    Retorna (resultado_em_JSON, success)
    """

    prompt = f"""
        Você é um analista de cibersegurança.

        Analise o seguinte conteúdo ({content_type}) e responda EXCLUSIVAMENTE em JSON válido.

        Formato obrigatório:
        {{
        "signals": ["..."],
        "risks": ["..."],
        "recommendations": ["..."],
        "summary": "resumo curto e objetivo"
        }}

        Regras:
        - Seja técnico e direto
        - Identifique sinais concretos
        - Liste riscos reais
        - Sugira recomendações práticas
        - NÃO escreva texto fora do JSON

        Conteúdo:
        {content}
    """

    try:
        result = client.query(prompt)
        parsed = json.loads(result)
        return parsed, True

    except Exception as e:
        return {
            "signals": ["Erro na análise LLM"],
            "risks": [],
            "recommendations": [],
            "summary": str(e)
        }, False