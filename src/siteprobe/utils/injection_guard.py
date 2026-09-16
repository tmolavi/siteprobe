import re


SUSPICIOUS_PROMPT_INJECTION_PATTERNS = [
    r"(?i)\bignore\s+(all\s+)?(previous|prior)\s+instructions\b",
    r"(?i)\byou\s+are\s+now\s+a\b",
    r"(?i)\bsystem\s+prompt\b",
    r"(?i)<\|\w+\|>",
    r"(?i)\[INST\].*?\[/INST\]",
    r"(?i)```(system|instruction)",
]


def sanitize_crawl_text(text: str) -> str:
    """
    Sanitize text extracted from public web pages before exposing it to AI agents.
    Neutralizes prompt injection directives by escaping delimiters and defanging instructions.
    """
    if not text:
        return ""
    sanitized = text
    for pat in SUSPICIOUS_PROMPT_INJECTION_PATTERNS:
        sanitized = re.sub(pat, "[UNTRUSTED_CONTENT_FILTERED]", sanitized)
    return sanitized
