# backend/orchestrator.py
from backend.analysis.engine import run_forensic_analysis
from backend.learning.memory_store import load_memory, save_memory
from backend.learning.embedding_engine import generate_embedding, cosine_similarity
from backend.learning.correlation_engine import analyze_correlation
from backend.llm.offline_mode import analyze_offline
from backend.llm.groq_llm import analyze_groq
from datetime import datetime
import numpy as np

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
                similar_logs.append({"content": log["content"], "similarity": sim})
    return similar_logs

def analyze(content, content_type="text", mode="offline-first", ip=None):
    memory = load_memory()
    if "logs" not in memory:
        memory["logs"] = []

    # 1️⃣ Offline
    result, success = analyze_offline(content, content_type, analysis_type=None, memory=memory)
    engine_used = "offline"

    # 2️⃣ Online fallback
    if not success and mode != "offline-only":
        result, _ = analyze_groq(content, content_type)
        engine_used = "groq"

    # 3️⃣ Criar entrada de memória
    timestamp = datetime.utcnow().isoformat()
    embedding = generate_embedding(str(content))
    memory_entry = {
        "timestamp": timestamp,
        "content": str(content),
        "content_type": content_type,
        "result": result,
        "engine_used": engine_used,
        "ip": ip,
        "embedding": embedding.tolist()
    }
    memory["logs"].append(memory_entry)

    # 4️⃣ Correlation
    alerts = analyze_correlation(memory, memory_entry)
    memory_entry["alerts"] = alerts

    # 5️⃣ Logs similares
    similar_logs = find_similar_logs(memory, memory_entry)
    if similar_logs:
        alerts.append(f"⚠️ {len(similar_logs)} logs semanticamente similares encontrados")
        memory_entry["similar_logs"] = similar_logs

    # 6️⃣ Salvar memória
    save_memory(memory)
    return result, engine_used, alerts