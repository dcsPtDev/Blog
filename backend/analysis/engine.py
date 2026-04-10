from backend.analysis.forensic.text_analysis import analyze_text_forensic
from backend.analysis.forensic.csv_analysis import analyze_csv_forensic
from backend.analysis.forensic.image_analysis import analyze_image_forensic
from backend.analysis.models import AnalysisReport


def run_forensic_analysis(content, content_type: str) -> AnalysisReport:
    if content_type == "text":
        report = analyze_text_forensic(str(content))
        return report

    if content_type == "csv":
        report = analyze_csv_forensic(str(content))
        return report

    if content_type == "image":
        import io
        image_bytes = io.BytesIO(content)
        return analyze_image_forensic(image_bytes)

    return AnalysisReport(
        artifact_type="unknown",
        findings=[],
        raw_evidence={"note": "content_type não reconhecido"}
    )