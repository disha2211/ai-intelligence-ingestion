from datetime import date
from typing import Any

from src.acquisition.models import RawRecord
from src.models.canonical import ResearchPaper


def parse_date(
    value: Any,
) -> date | None:

    if not value:
        return None

    if isinstance(value, date):
        return value

    value = str(value).strip()

    # ISO datetime:
    # 2026-08-30T12:30:00Z
    try:
        return date.fromisoformat(
            value[:10]
        )
    except ValueError:
        return None


def normalize_paper(
    record: RawRecord,
) -> ResearchPaper:

    data = record.payload

    title = (
        data.get("title")
        or ""
    ).strip()

    abstract = (
        data.get("abstract")
        or data.get("summary")
        or ""
    ).strip()

    authors = data.get("authors") or []

    if isinstance(authors, str):
        authors = [authors]

    authors = [
        str(author).strip()
        for author in authors
        if str(author).strip()
    ]

    published = (
        data.get("published_date")
        or data.get("published")
        or data.get("date")
    )

    return ResearchPaper(
        title=title,
        authors=authors,
        abstract=abstract,
        url=(
            data.get("paper_url")
            or data.get("url")
            or record.source_url
        ),
        source=record.source_name,
        published_date=parse_date(
            published
        ),
        github_url=data.get(
            "github_url"
        ),
        github_stars=data.get(
            "github_stars"
        ),
    )