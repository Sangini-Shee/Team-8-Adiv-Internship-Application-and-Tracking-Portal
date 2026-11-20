
import re


SUSPICIOUS_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(the\s+)?(system\s+)?prompt",
    r"bypass\s+(the\s+)?(security|safety|policy)",
    r"disable\s+(all\s+)?safety",
    r"expose\s+(passwords|api\s+keys|secrets)",
    r"steal\s+(credentials|passwords)",
]


def validate_input(user_input):
    """Validate user input before processing."""

    if not isinstance(user_input, str):
        return {
            "safe": False,
            "status": "blocked",
            "reason": "Input must be text."
        }

    if not user_input.strip():
        return {
            "safe": False,
            "status": "blocked",
            "reason": "Input cannot be empty."
        }

    if len(user_input) > 5000:
        return {
            "safe": False,
            "status": "blocked",
            "reason": "Input exceeds the maximum allowed length."
        }

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return {
                "safe": False,
                "status": "blocked",
                "reason": "Potentially unsafe instruction detected."
            }

    return {
        "safe": True,
        "status": "approved",
        "reason": "Input passed safety validation."
    }
