from __future__ import annotations

from urllib.parse import urlparse


def normalize_url(value: str) -> str:
    url = value.strip()
    if not url:
        raise ValueError("URL is empty")
    parsed = urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http:// and https:// URLs are supported")
    if not parsed.netloc:
        raise ValueError("URL does not contain a host")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing embedded credentials are not supported")
    return url


def is_supported_url(value: str) -> bool:
    try:
        normalize_url(value)
    except (TypeError, AttributeError, ValueError):
        return False
    return True
