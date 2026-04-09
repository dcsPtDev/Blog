# backend/learning/correlation_engine.py
from typing import Dict, Any, List

def jaccard_similarity(a: str, b: str) -> float:
    """
    Calcula similaridade Jaccard entre dois textos.
    Retorna valor entre 0 e 1.
    """
    set_a = set(a.split())
    set_b = set(b.split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def analyze_correlation(memory: Dict[str, Any], new_entry: Dict[str, Any]) -> List[str]:
    """
    Analisa o log recém-chegado em relação à memória.
    Gera alertas com base em:
        - IP reincidente
        - Padrões repetidos
        - Conteúdo suspeito (alta entropia)
    """
    alerts: List[str] = []
    content = new_entry.get("content", "")
    ip = new_entry.get("ip")

    # 1️⃣ Reincidência de IP
    if ip:
        ip_count = memory.get("ips", {}).get(ip, 0)
        if ip_count >= 3:
            alerts.append(f"⚠️ IP {ip} reincidente ({ip_count} ocorrências)")

    # 2️⃣ Padrões similares em logs recentes
    recent_logs = memory.get("logs", [])[-20:]  # últimos 20 logs
    similar_count = 0
    for log in recent_logs:
        sim = jaccard_similarity(content, log.get("content", ""))
        if sim > 0.7:  # limiar de similaridade
            similar_count += 1
    if similar_count >= 2:
        alerts.append("⚠️ Padrão repetido em logs recentes")

    # 3️⃣ Conteúdos suspeitos já marcados (ex.: alta entropia)
    if "Alta entropia" in new_entry.get("result", ""):
        alerts.append("⚠️ Conteúdo de alta entropia detectado")

    return alerts