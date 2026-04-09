# backend/analysis/forensic/text_analysis.py
from backend.analysis.models import Finding, AnalysisReport
from backend.analysis.detectors.ip_analysis import detect_ips
from backend.analysis.detectors.auth_analysis import detect_auth_failures
from backend.analysis.detectors.encoding_analysis import entropy, detect_base64


def analyze_text_forensic(text: str) -> AnalysisReport:
    """
    Realiza análise forense de logs de texto.
    
    Detecta:
      - IPs
      - Falhas de autenticação
      - Conteúdo de alta entropia (possível ofuscação)
      - Conteúdo codificado em Base64
    """
    report = AnalysisReport(artifact_type="text_log")

    # ---------- Detecta IPs ----------
    ips = detect_ips(text)
    if ips:
        report.findings.append(
            Finding(
                category="network",
                severity="medium",
                description="Endereços IP detectados no conteúdo",
                evidence=", ".join(ips),
                confidence=0.6
            )
        )

    # ---------- Detecta falhas de autenticação ----------
    if detect_auth_failures(text):
        report.findings.append(
            Finding(
                category="authentication",
                severity="high",
                description="Falha de autenticação detectada",
                evidence=text.strip()[:200],
                confidence=0.8
            )
        )

    # ---------- Detecta alta entropia ----------
    ent = entropy(text)
    if ent > 4.5:
        report.findings.append(
            Finding(
                category="obfuscation",
                severity="medium",
                description="Alta entropia — possível conteúdo ofuscado",
                evidence=f"Entropy={ent:.2f}",
                confidence=0.7
            )
        )

    # ---------- Detecta Base64 ----------
    if detect_base64(text):
        report.findings.append(
            Finding(
                category="encoding",
                severity="medium",
                description="Conteúdo aparenta estar codificado em Base64",
                evidence=text[:100],
                confidence=0.75
            )
        )

    # ---------- Fallback ----------
    if not report.findings:
        report.findings.append(
            Finding(
                category="text_log",
                severity="info",
                description="Nenhum sinal forense detectado",
                evidence=text[:200],
                confidence=0.5
            )
        )

    return report