import re
from typing import Any, Dict


SENSITIVE_PATTERNS = [
    r"(?i)(api[-_]?key|auth[-_]?token|password|secret|bearer|access[-_]?token)[\s:=]+['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?",
    r"(?i)gh[pousr]_[A-Za-z0-9_]{36,}",
    r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}",
]


def redact_sensitive_string(text: str) -> str:
    """Redact passwords, tokens, and authorization strings from text."""
    if not text:
        return text
    cleaned = text
    for pattern in SENSITIVE_PATTERNS:
        cleaned = re.sub(pattern, r"\1: [REDACTED]", cleaned)
    return cleaned


def redact_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Redact authorization, cookie, and proxy headers."""
    redacted = {}
    for k, v in headers.items():
        k_lower = k.lower()
        if any(secret_term in k_lower for secret_term in ("authorization", "cookie", "set-cookie", "proxy-authorization", "x-api-key")):
            redacted[k] = "[REDACTED]"
        else:
            redacted[k] = v
    return redacted
