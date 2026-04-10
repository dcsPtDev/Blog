# # backend/analysis/forensic/image_analysis.py

import io
import re
import math
from PIL import Image
from backend.analysis.models import AnalysisReport, Finding


def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    ent = 0.0
    for count in freq.values():
        p = count / len(data)
        ent -= p * math.log2(p)
    return ent


def extract_strings(data: bytes, min_len: int = 6) -> list[str]:
    pattern = rb"[ -~]{" + str(min_len).encode() + rb",}"
    return [s.decode(errors="ignore") for s in re.findall(pattern, data)]


def analyze_image_forensic(image_bytes: io.BytesIO) -> AnalysisReport:
    report = AnalysisReport(
        artifact_type="image",
        raw_evidence={}
    )

    data = image_bytes.read()
    report.raw_evidence["byte_size"] = len(data)

    ent = calculate_entropy(data)
    report.raw_evidence["entropy"] = round(ent, 2)
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

    strings = extract_strings(data)
    if strings:
        report.raw_evidence["hidden_strings"] = strings[:20]
        report.findings.append(
            Finding(
                category="hidden_data",
                severity="medium",
                description="Possíveis strings ocultas encontradas",
                evidence=" | ".join(strings[:5]),
                confidence=0.6
            )
        )

    signatures = {
        b"PK\x03\x04": "ZIP",
        b"%PDF": "PDF",
        b"\x89PNG": "PNG",
        b"GIF89a": "GIF"
    }

    embedded_files = []
    for sig, name in signatures.items():
        if sig in data:
            embedded_files.append(name)
            report.findings.append(
                Finding(
                    category="embedded_file",
                    severity="high",
                    description="Possível ficheiro embutido na imagem",
                    evidence=name,
                    confidence=0.8
                )
            )
    if embedded_files:
        report.raw_evidence["embedded_files"] = embedded_files

    try:
        img = Image.open(io.BytesIO(data))
        exif = img.getexif()
        if exif:
            exif_dict = {}
            for k, v in exif.items():
                exif_dict[str(k)] = str(v)
            report.raw_evidence["exif"] = exif_dict
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
        pass

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