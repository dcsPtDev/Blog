from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Finding:
    category: str
    severity: str = "medium"
    description: str = ""
    evidence: str = ""
    confidence: float = 0.5


@dataclass
class AnalysisReport:
    artifact_type: str
    findings: List[Finding] = field(default_factory=list)
    raw_evidence: dict = field(default_factory=dict)

    def risk_level(self) -> str:
        if not self.findings:
            return "low"
        severities = [f.severity.lower() for f in self.findings]
        if "high" in severities:
            return "high"
        if "medium" in severities:
            return "medium"
        return "low"

    def to_dict(self) -> dict:
        return {
            "artifact_type": self.artifact_type,
            "risk_level": self.risk_level(),
            "findings": [
                {
                    "category": f.category,
                    "severity": f.severity,
                    "description": f.description,
                    "evidence": f.evidence,
                    "confidence": f.confidence,
                }
                for f in self.findings
            ],
            "raw_evidence": self.raw_evidence,
        }