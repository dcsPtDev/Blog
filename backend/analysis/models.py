# backend/analysis/models.py

from dataclasses import dataclass
from typing import List

@dataclass
class Finding:
    description: str
    severity: str = "medium"

@dataclass
class AnalysisReport:
    findings: List[Finding]

    def risk_level(self):
        if not self.findings:
            return "low"
        severities = [f.severity for f in self.findings]
        if "high" in severities:
            return "high"
        if "medium" in severities:
            return "medium"
        return "low"