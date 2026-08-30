from typing import Any
from urllib.parse import urlparse
from src.acquisition.models import RawRecord
from src.models.canonical import Startup
from src.normalization.utils import (
    normalize_url,
)


def optional_string(value: Any) -> str | None:
    """
    Convert missing/blank values to None.
    """
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        return value if value else None

    return str(value).strip() or None


def normalize_startup(
    record: RawRecord,
) -> Startup | None:

    data: dict[str, Any] = record.payload

    name = (
        data.get("name")
        or data.get("company_name")
        or ""
    ).strip()

    if not name:
        return None

    description = (
        data.get("description")
        or data.get("long_description")
        or ""
    ).strip()

    url = normalize_url(
        data.get("website")
        or data.get("url")
        or ""
    )

    if url is None:
        print(
            f"Skipping startup without "
            f"valid URL: {name}"
        )
        return None

    founders = data.get("founders") or []

    if isinstance(founders, str):
        founders = [founders]

    founders = [
        str(founder).strip()
        for founder in founders
        if str(founder).strip()
    ]

    founded_year = data.get(
        "founded_year"
    )

    if founded_year:
        try:
            founded_year = int(
                founded_year
            )
        except (TypeError, ValueError):
            founded_year = None

    linkedin_url = normalize_url(
        data.get("linkedin_url")
    )

    return Startup(
        name=name,
        description=description,
        url=url,
        source=record.source_name,
        industry=(
            data.get("industry")
            or data.get("industries")
        ),
        founded_year=founded_year,
        location=(
            data.get("location")
            or data.get("city")
        ),
        funding_stage=(
            data.get("funding_stage")
            or data.get("stage")
        ),
        founders=founders,
        linkedin_url=linkedin_url,
    )


def is_valid_url(
    value: str,
) -> bool:

    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in {
                "http",
                "https",
            }
            and bool(parsed.netloc)
        )

    except ValueError:
        return False

