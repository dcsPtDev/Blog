# backend/analysis/detectors/auth.py
def detect_auth_failures(text: str) -> bool:
    keywords = ["failed password", "login failed", "authentication failure", "denied"]
    text_lower = text.lower()
    return any(k in text_lower for k in keywords)
