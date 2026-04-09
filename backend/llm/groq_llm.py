# backend/llm/groq_llm.py
from backend.llm.groq_client import GroqClient

client = GroqClient()

def analyze_groq(content, content_type: str):
    """
    Envia conteúdo ao Groq.
    Retorna (resultado, success)
    """
    prompt = f"""
Você é um analista de cybersecurity.
Analise o seguinte artefacto do tipo: {content_type}

Conteúdo:
{content}

Forneça uma análise clara, objetiva, focada em segurança,
identifique riscos, vulnerabilidades e boas práticas.

Responda de forma concisa, sem rodeios, e destaque pontos críticos.
    """

    try:
        result = client.query(prompt)
        if result:
            return result, True
        return "Groq retornou resposta vazia.", False
    except Exception as e:
        return f"Erro ao chamar Groq: {e}", False