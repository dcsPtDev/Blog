# backend/analysis/forensic/csv_analysis.py

from backend.analysis.models import AnalysisReport, Finding


def analyze_csv_forensic(csv_text: str) -> AnalysisReport:
    """
    Analisa um CSV e gera um relatório forense básico:
      - Estrutura do arquivo
      - Presença de dados
      - Futuro: validação de campos, detecção de padrões maliciosos
    """
    lines = csv_text.strip().splitlines()
    report = AnalysisReport(artifact_type="csv")

    # ---------- CSV vazio ou apenas cabeçalho ----------
    if len(lines) <= 1:
        report.findings.append(
            Finding(
                category="structure",
                severity="low",
                description="CSV vazio ou sem dados",
                evidence="Linhas <= 1",
                confidence=0.9
            )
        )
        return report

    # ---------- CSV com dados ----------
    report.findings.append(
        Finding(
            category="structure",
            severity="low",
            description="CSV contém dados estruturados",
            evidence=f"{len(lines)-1} linhas de dados",
            confidence=0.95
        )
    )

    # ---------- Possível extensão ----------
    # Aqui poderíamos adicionar:
    # - Checagem de colunas esperadas
    # - Detecção de valores suspeitos
    # - Detecção de headers maliciosos ou injetados

    return report