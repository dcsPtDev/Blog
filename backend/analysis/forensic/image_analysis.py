# backend/analysis/forensic/image_analysis.py

import io
import re
import math
from PIL import Image
from backend.analysis.models import AnalysisReport, Finding


def calculate_entropy(data: bytes) -> float:
    """Calcula a entropia de bytes de uma imagem."""
    if not data:
        return 0.0

    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1

    entropy = 0.0
    for count in freq.values():
        p = count / len(data)
        entropy -= p * math.log2(p)

    return entropy


def extract_strings(data: bytes, min_len: int = 6) -> list[str]:
    """Extrai strings legíveis em ASCII/UTF-8 da imagem."""
    pattern = rb"[ -~]{" + str(min_len).encode() + rb",}"
    return [s.decode(errors="ignore") for s in re.findall(pattern, data)]


def analyze_image_forensic(image_bytes: io.BytesIO) -> AnalysisReport:
    """
    Analisa uma imagem em busca de sinais forenses:
      - alta entropia (possível steganografia)
      - strings ocultas
      - arquivos embutidos
      - metadados EXIF
    """
    report = AnalysisReport(artifact_type="image")
    data = image_bytes.read()

    # ---------- Entropy Analysis ----------
    ent = calculate_entropy(data)
    if ent > 7.5:
        report.findings.append(
            Finding(
                category="steganography",
                severity="medium",
                description="Alta entropia detectada na imagem",
                evidence=f"Entropy={ent:.2f}",
                confidence=0.7
            )
        )

    # ---------- Strings Ocultas ----------
    strings = extract_strings(data)
    if strings:
        report.findings.append(
            Finding(
                category="hidden_data",
                severity="medium",
                description="Possíveis strings ocultas encontradas",
                evidence=", ".join(strings[:5]),
                confidence=0.6
            )
        )

    # ---------- Assinaturas de Arquivos Embutidos ----------
    signatures = {
        b"PK\x03\x04": "ZIP",
        b"%PDF": "PDF",
        b"\x89PNG": "PNG",
        b"GIF89a": "GIF"
    }
    for sig, name in signatures.items():
        if sig in data:
            report.findings.append(
                Finding(
                    category="embedded_file",
                    severity="high",
                    description="Possível ficheiro embutido na imagem",
                    evidence=name,
                    confidence=0.8
                )
            )

    # ---------- Metadados EXIF ----------
    try:
        img = Image.open(io.BytesIO(data))
        exif = img.getexif()
        if exif:
            report.findings.append(
                Finding(
                    category="metadata",
                    severity="low",
                    description="Metadados EXIF presentes",
                    evidence=f"{len(exif)} campos EXIF",
                    confidence=0.9
                )
            )
    except Exception:
        pass  # Falha ao abrir imagem ou ler EXIF não é crítica

    # ---------- Fallback ----------
    if not report.findings:
        report.findings.append(
            Finding(
                category="image",
                severity="info",
                description="Nenhuma evidência de steganografia ou dados ocultos detectada",
                evidence="Análise básica concluída",
                confidence=0.5
            )
        )

    return report