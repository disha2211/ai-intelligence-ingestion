from collections.abc import Iterable
from urllib.parse import urlparse

from src.models.canonical import (
    Product,
    ResearchPaper,
    Startup,
)


def canonical_url(url: str) -> str:
    parsed = urlparse(str(url))

    host = parsed.netloc.lower().replace(
        "www.",
        "",
    )

    path = parsed.path.rstrip("/").lower()

    return f"{host}{path}"


def deduplicate(
    records: Iterable,
):
    seen_urls: set[str] = set()
    seen_names: set[str] = set()

    result = []

    for record in records:

        url_key = canonical_url(
            str(record.url)
        )

        name_key = (
            getattr(record, "name", None)
            or getattr(record, "title", "")
        ).strip().lower()

        if (
            url_key in seen_urls
            or (
                name_key
                and name_key in seen_names
            )
        ):
            continue

        seen_urls.add(url_key)

        if name_key:
            seen_names.add(name_key)

        result.append(record)

    return result