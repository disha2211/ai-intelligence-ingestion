from typing import Any
from urllib.parse import urlparse


def normalize_url(
    value: Any,
) -> str | None:

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    if not value.startswith(
        ("http://", "https://")
    ):
        value = f"https://{value}"

    parsed = urlparse(value)

    if not parsed.netloc:
        return None

    return value