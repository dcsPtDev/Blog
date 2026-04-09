# backend/learning/learner.py
from backend.learning.embedding_engine import generate_embedding, cosine_similarity

SIMILARITY_THRESHOLD = 0.80  # Limite para considerar eventos semelhantes

def learn_and_compare(report, memory):
    """
    Aprende com o report atual e verifica similaridade com eventos anteriores.

    Args:
        report: AnalysisReport, resultado da análise forense.
        memory: dict, memória com 'semantic_memory' para eventos passados.

    Returns:
        insights: list de strings com observações sobre eventos semelhantes.
    """
    insights = []

    # Resumir o conteúdo do report em uma string representativa
    summary = " ".join(f.description for f in report.findings)
    if not summary:
        return insights  # Nenhum dado para aprender

    # Gerar embedding para o resumo atual
    current_vec = generate_embedding(summary)

    # Recupera eventos passados da memória
    past_events = memory.get("semantic_memory", [])

    for event in past_events:
        past_vec = event.get("embedding")
        if past_vec:
            # Converter para numpy array
            import numpy as np
            past_vec = np.array(past_vec)
            sim = cosine_similarity(current_vec, past_vec)
            if sim >= SIMILARITY_THRESHOLD:
                insights.append(
                    f"⚠️ Evento semelhante já observado (similaridade {sim:.2f})"
                )

    # Aprender: adicionar novo embedding à memória
    memory.setdefault("semantic_memory", []).append({
        "summary": summary,
        "embedding": current_vec.tolist(),
        "risk": report.risk_level()
    })

    return insights