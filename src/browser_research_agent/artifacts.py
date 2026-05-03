from __future__ import annotations

import hashlib
import re
from urllib.parse import urlparse

_SAFE_RE = re.compile(r"[^a-z0-9]+")


def safe_slug(url: str, index: int) -> str:
    """Create a readable, filesystem-safe, collision-resistant page artifact slug."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower() or "unknown-url"
    domain = domain.split("@")[-1].split(":")[0]
    readable = _SAFE_RE.sub("-", domain).strip("-") or "unknown-url"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]
    return f"{index:02d}-{readable[:48]}-{digest}"
