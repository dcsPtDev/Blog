# backend/analysis/detectors/ip.py
import re

IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

def detect_ips(text: str) -> list[str]:
    return list(set(re.findall(IP_PATTERN, text)))
