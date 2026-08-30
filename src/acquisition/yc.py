from collections.abc import AsyncIterator
from datetime import datetime, timezone
from typing import Any

import aiohttp

from src.acquisition.base import AcquisitionSource
from src.acquisition.models import RawRecord


class YCStartupSource(AcquisitionSource):
    """
    Acquisition source for publicly listed Y Combinator companies.

    The upstream dataset is a public JSON representation of
    YC's company directory.
    """

    name = "y_combinator"
    entity_type = "STARTUP"

    URL = (
        "https://devasheeshg.github.io/"
        "yc-api/companies/all.json"
    )

    async def fetch(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[RawRecord]:

        timeout = aiohttp.ClientTimeout(
            total=60
        )

        headers = {
            "User-Agent": (
                "AI-Intelligence-Pipeline/1.0"
            )
        }

        collected_at = datetime.now(
            timezone.utc
        )

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
        ) as session:

            async with session.get(
                self.URL
            ) as response:

                response.raise_for_status()

                data: list[dict[str, Any]] = (
                    await response.json()
                )

        start = int(cursor or 0)

        if limit is None:
            end = len(data)
        else:
            end = min(
                start + limit,
                len(data),
            )

        for company in data[start:end]:

            name = self._get_name(company)

            website = self._get_website(
                company
            )

            if not name or not website:
                continue

            yield RawRecord(
                        source_name=self.name,
                        source_url=self.URL,
                        canonical_url=website,
                        entity_type=self.entity_type,
                        payload=company,
                        collected_at=collected_at,
                    )

    @staticmethod
    def _get_name(
        company: dict[str, Any],
    ) -> str:

        for key in (
            "name",
            "company_name",
        ):

            value = company.get(key)

            if isinstance(value, str):
                value = value.strip()

                if value:
                    return value

        return ""

    @staticmethod
    def _get_website(
        company: dict[str, Any],
    ) -> str:

        for key in (
            "website",
            "url",
        ):

            value = company.get(key)

            if isinstance(value, str):
                value = value.strip()

                if value.startswith(
                    "http://"
                ) or value.startswith(
                    "https://"
                ):
                    return value

        return ""