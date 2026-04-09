# backend/analysis/detectors/encoding.py
import re
import math
from collections import Counter

def entropy(text: str) -> float:
    if not text:
        return 0
    counts = Counter(text)
    total = len(text)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def detect_base64(text: str) -> bool:
    return len(text) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/=]+", text) is not None
