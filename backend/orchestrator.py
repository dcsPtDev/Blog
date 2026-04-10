
from datetime import datetime
import uuid
import numpy as np

from backend.learning.memory_store import load_memory, save_memory
from backend.learning.embedding_engine import generate_embedding, cosine_similarity
from backend.learning.correlation_engine import analyze_correlation
from backend.analysis.engine import run_forensic_analysis
from backend.analysis.local_llm import analyze_local_llm
from backend.llm.groq_llm import analyze_groq


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


def format_finding_summary(report):
    lines = [f"Artefacto: {report.artifact_type}", f"Risco: {report.risk_level()}"]
    for f in report.findings:
        lines.append(
            f"- [{f.severity}] {f.category}: {f.description} | Evidência: {f.evidence} | Confiança: {f.confidence}"
        )
    return "\n".join(lines)


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
    if analysis.get("summary"):
        text += f"\nResumo\n- {analysis['summary']}\n"
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

    forensic_report = run_forensic_analysis(content, content_type)
    forensic_dict = forensic_report.to_dict()
    forensic_summary = format_finding_summary(forensic_report)

    engine_used = "forensic-only"
    analysis = {
        "signals": [],
        "risks": [],
        "recommendations": [],
        "summary": forensic_summary
    }

    if mode in ["offline-first", "offline-only"]:
        llm_output = analyze_local_llm(forensic_dict)
        analysis = safe_parse_json(llm_output)
        engine_used = "local"

    if mode != "offline-only":
        if not analysis.get("risks") and not analysis.get("recommendations"):
            groq_result, success_online = analyze_groq(forensic_summary, content_type)
            online_analysis = safe_parse_json(groq_result)
            if success_online and online_analysis:
                analysis = online_analysis
                engine_used = "groq"

    if not analysis.get("summary"):
        analysis["summary"] = forensic_summary[:300]

    embedding = generate_embedding(forensic_summary)

    timestamp = datetime.utcnow().isoformat()
    memory_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "type": content_type,
        "content": str(content)[:1000],
        "forensic_report": forensic_dict,
        "analysis": analysis,
        "result": format_analysis_text(analysis),
        "summary": analysis.get("summary", ""),
        "engine": engine_used,
        "ip": ip,
        "embedding": embedding.tolist(),
        "findings": analysis.get("risks", []),
        "risk_score": calculate_risk(analysis)
    }

    alerts = analyze_correlation(memory, {
        "content": forensic_summary,
        "ip": ip,
        "result": memory_entry["result"]
    })
    memory_entry["alerts"] = alerts

    similar_logs = find_similar_logs(memory, memory_entry)
    if similar_logs:
        alerts.append(f"{len(similar_logs)} logs similares encontrados")
        memory_entry["similar_logs"] = similar_logs

    memory["logs"].append(memory_entry)
    save_memory(memory)

    return memory_entry["result"], engine_used, alerts, forensic_dict