from backend.learning.memory_store import load_memory, save_memory
from backend.learning.embedding_engine import generate_embedding, cosine_similarity
from backend.learning.correlation_engine import analyze_correlation
from backend.llm.offline_mode import analyze_offline
from backend.llm.groq_llm import analyze_groq

from datetime import datetime
import numpy as np
import uuid
import json

# def safe_parse_json(text):
#     try:
#         return json.loads(text)
#     except:
#         return {
#             "signals": [text[:100]],
#             "risks": [],
#             "recommendations": [],
#             "summary": text[:200]
#         }
def safe_parse_json(obj):
    import json
    if isinstance(obj, dict):
        return obj
    try:
        return json.loads(obj)
    except Exception:
        return {
            "signals": [str(obj)[:100]],
            "risks": [],
            "recommendations": [],
            "summary": str(obj)[:200]
        }

def format_analysis_text(analysis):
    text = "Análise de Segurança\n\n"
    if analysis.get("signals"):
        text += "Sinais Detectados\n"
        for s in analysis["signals"]:
            text += f"- {s}\n"
    if analysis.get("risks"):
        text += "\nRiscos Potenciais\n"
        for r in analysis["risks"]:
            text += f"- {r}\n"
    if analysis.get("recommendations"):
        text += "\nRecomendações\n"
        for rec in analysis["recommendations"]:
            text += f"- {rec}\n"
    return text

def find_similar_logs(memory, new_entry, threshold=0.75):
    similar_logs = []
    new_vec = new_entry.get("embedding")
    if new_vec is None:
        return similar_logs
    for log in memory.get("logs", []):
        vec = log.get("embedding")
        if vec is not None:
            sim = cosine_similarity(np.array(new_vec), np.array(vec))
            if sim >= threshold:
                similar_logs.append({
                    "id": log.get("id"),
                    "similarity": float(sim)
                })
    return similar_logs

def calculate_risk(analysis):
    alerts = analysis.get("risks", [])
    if not alerts:
        return 0.1
    score = min(1.0, 0.2 + 0.15 * len(alerts))
    for r in alerts:
        if "critical" in r.lower():
            score += 0.2
        if "ip" in r.lower():
            score += 0.1
    return round(min(score, 1.0), 2)

def analyze(content, content_type="text", mode="offline-first", ip=None):
    memory = load_memory()
    if "logs" not in memory:
        memory["logs"] = []

    # 1️⃣ Offline
    analysis, success = analyze_offline(content, content_type, memory=memory)
    engine_used = "offline"

    # # 2️⃣ Online fallback se offline não encontrar sinais
    # if not success and mode != "offline-only":
    #     groq_result, success_online = analyze_groq(content, content_type)
    #     online_analysis = safe_parse_json(groq_result)
    #     if success_online:
    #         analysis = online_analysis
    #         engine_used = "groq"
    # Online fallback
    if not success and mode != "offline-only":
        groq_result, success_online = analyze_groq(content, content_type)

        if isinstance(groq_result, str):
            #online_analysis = safe_parse_json(groq_result)
            analysis = safe_parse_json(groq_result)
        else:
            #online_analysis = groq_result
            analysis = groq_result
        if success_online:
            #analysis = online_analysis
            engine_used = "groq"

    # 3️⃣ Embedding
    embedding = generate_embedding(str(content))

    # 4️⃣ Memória
    timestamp = datetime.utcnow().isoformat()
    memory_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "type": content_type,
        "content": str(content)[:1000],
        "analysis": analysis,
        "result": format_analysis_text(analysis),
        "summary": analysis.get("summary", ""),
        "engine": engine_used,
        "ip": ip,
        "embedding": embedding.tolist(),
        "findings": analysis.get("risks", [])
    }

    # 5️⃣ Correlation
    alerts = analyze_correlation(memory, memory_entry)
    memory_entry["alerts"] = alerts

    # 6️⃣ Similaridade
    similar_logs = find_similar_logs(memory, memory_entry)
    if similar_logs:
        alerts.append(f"{len(similar_logs)} logs similares encontrados")
        memory_entry["similar_logs"] = similar_logs

    # 7️⃣ Risco
    memory_entry["risk_score"] = calculate_risk(analysis)

    # 8️⃣ Salvar memória
    memory["logs"].append(memory_entry)
    save_memory(memory)

    return memory_entry["result"], engine_used, alerts