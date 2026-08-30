from typing import Any

from src.acquisition.models import RawRecord
from src.models.canonical import Startup


def normalize_startup(
    record: RawRecord,
) -> Startup:

    data: dict[str, Any] = record.payload

    name = (
        data.get("name")
        or data.get("company_name")
        or ""
    ).strip()

    description = (
        data.get("description")
        or data.get("long_description")
        or ""
    ).strip()

    url = (
        data.get("website")
        or data.get("url")
        or record.source_url
    )

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
        linkedin_url=data.get(
            "linkedin_url"
        ),
    )