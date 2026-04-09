#backend/llm/offline_mode.py

import re
from typing import Tuple, Dict, Any

def analyze_offline(
    content,
    content_type: str,
    analysis_type: str | None,
    memory: Dict[str, Any]
) -> Tuple[str, bool]:

    signals = []
    risks = []
    recommendations = []

    # -----------------------------
    # TEXT / LOG ANALYSIS
    # -----------------------------
    if content_type == "text":
        text = str(content)
        text_lower = text.lower()

        # eventos de erro
        if any(k in text_lower for k in ["erro", "denied", "falha", "failed"]):
            signals.append("Eventos de erro ou falha de acesso detectados.")
            risks.append("Possível problema de autenticação ou permissões.")

        # login falhado
        if "login" in text_lower and ("falha" in text_lower or "failed" in text_lower):
            signals.append("Tentativa de login falhada identificada.")
            risks.append("Possível tentativa de brute force ou credenciais inválidas.")
            recommendations.append(
                "Monitorizar múltiplas falhas de login e aplicar rate limiting."
            )

        # IPs
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ips = list(set(re.findall(ip_pattern, text)))
        if ips:
            signals.append(f"Endereços IP detectados: {', '.join(ips)}")
            risks.append("IPs podem indicar origem de acesso ou atividade suspeita.")
            recommendations.append("Verificar reputação dos IPs e padrões de acesso.")

    # -----------------------------
    # CSV
    # -----------------------------
    elif content_type == "csv":
        lines = str(content).strip().splitlines()
        if len(lines) > 1:
            signals.append(f"CSV contém {len(lines)-1} linhas de dados.")
        else:
            signals.append("CSV contém apenas cabeçalho ou está vazio.")

    # -----------------------------
    # IMAGE
    # -----------------------------
    elif content_type == "image":
        signals.append("Imagem recebida para análise.")
        recommendations.append("Utilizar OCR ou análise visual para extrair informação relevante.")

    # -----------------------------
    # BUILD RESPONSE
    # -----------------------------
    if not signals:
        signals.append("Nenhum sinal relevante identificado.")

    result = "Análise de Segurança\n\n"
    result += "Sinais Detectados\n"
    for s in signals:
        result += f"- {s}\n"
    if risks:
        result += "\nRiscos Potenciais\n"
        for r in risks:
            result += f"- {r}\n"
    if recommendations:
        result += "\nRecomendações\n"
        for rec in recommendations:
            result += f"- {rec}\n"

    return result, True