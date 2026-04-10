# # backend/analysis/forensic/text_analysis.py


from backend.analysis.models import Finding, AnalysisReport
from backend.analysis.detectors.ip_analysis import detect_ips
from backend.analysis.detectors.auth_analysis import detect_auth_failures
from backend.analysis.detectors.encoding_analysis import entropy, detect_base64


def analyze_text_forensic(text: str) -> AnalysisReport:
    report = AnalysisReport(
        artifact_type="text_log",
        raw_evidence={"text_sample": text[:1000]}
    )

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
        report.raw_evidence["ips"] = ips

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

    ent = entropy(text)
    report.raw_evidence["entropy"] = round(ent, 2)
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

