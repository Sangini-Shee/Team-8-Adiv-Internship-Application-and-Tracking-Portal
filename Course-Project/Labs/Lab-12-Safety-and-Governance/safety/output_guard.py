
import re


SENSITIVE_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
    "api_key": r"\b(?:AIza[0-9A-Za-z_-]{30,}|sk-[A-Za-z0-9_-]{20,})\b",
}


def validate_output(output):
    """Check generated output for sensitive information."""

    if not isinstance(output, str):
        return {
            "safe": False,
            "status": "blocked",
            "reason": "Output must be text."
        }

    if not output.strip():
        return {
            "safe": False,
            "status": "blocked",
            "reason": "Generated output is empty."
        }

    detected = []

    for category, pattern in SENSITIVE_PATTERNS.items():
        if re.search(pattern, output):
            detected.append(category)

    if detected:
        return {
            "safe": False,
            "status": "blocked",
            "reason": "Sensitive information detected.",
            "detected_categories": detected
        }

    return {
        "safe": True,
        "status": "approved",
        "reason": "Output passed safety validation.",
        "detected_categories": []
    }
