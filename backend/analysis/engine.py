# backend/analysis/engine.py
from backend.analysis.forensic.text_analysis import analyze_text_forensic
from backend.analysis.forensic.csv_analysis import analyze_csv_forensic
from backend.analysis.forensic.image_analysis import analyze_image_forensic
from backend.analysis.models import AnalysisReport

def run_forensic_analysis(content, content_type: str) -> AnalysisReport:
    """
    Roteia a análise de conteúdo para o analisador adequado.
    
    content_type: "text", "csv", "image"
    """
    if content_type == "text":
        return analyze_text_forensic(str(content))

    if content_type == "csv":
        return analyze_csv_forensic(str(content))

    if content_type == "image":
        # Para imagens, content deve ser um objeto tipo BytesIO ou arquivo binário
        return analyze_image_forensic(content)

    # Se não reconhecido
    return AnalysisReport(artifact_type="unknown")