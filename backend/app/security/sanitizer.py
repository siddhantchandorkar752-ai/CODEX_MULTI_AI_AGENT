from __future__ import annotations

import re


INJECTION_PATTERNS = [
    re.compile(r"ignore (all )?(previous|prior) instructions", re.IGNORECASE),
    re.compile(r"system prompt", re.IGNORECASE),
    re.compile(r"developer message", re.IGNORECASE),
    re.compile(r"exfiltrate|leak|secret|api key", re.IGNORECASE),
]


def sanitize_untrusted_text(text: str) -> tuple[str, list[str]]:
    findings: list[str] = []
    sanitized = text
    for pattern in INJECTION_PATTERNS:
        if pattern.search(sanitized):
            findings.append(pattern.pattern)
            sanitized = pattern.sub("[removed unsafe instruction]", sanitized)
    sanitized = re.sub(r"<script.*?</script>", "", sanitized, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized, findings
