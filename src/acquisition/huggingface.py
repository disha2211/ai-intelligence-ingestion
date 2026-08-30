from collections.abc import AsyncIterator
from datetime import datetime, timezone
from typing import Any

import aiohttp

from src.acquisition.base import AcquisitionSource
from src.acquisition.models import RawRecord


class HuggingFaceSource(AcquisitionSource):

    BASE_URL = "https://huggingface.co/api"

    def __init__(
        self,
        entity_type: str,
        endpoint: str,
        source_name: str,
    ) -> None:
        self.entity_type = entity_type
        self.endpoint = endpoint
        self.name = source_name

    async def fetch(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[RawRecord]:

        collected_at = datetime.now(
            timezone.utc
        )

        start = int(cursor or 0)

        remaining = limit

        timeout = aiohttp.ClientTimeout(
            total=60
        )

        headers = {
            "User-Agent": (
                "AI-Intelligence-Pipeline/1.0"
            )
        }

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
        ) as session:

            while (
                remaining is None
                or remaining > 0
            ):

                params: dict[str, Any] = {
                    "limit": 100,
                    "offset": start,
                }

                if remaining is not None:
                    params["limit"] = min(
                        100,
                        remaining,
                    )

                url = (
                    f"{self.BASE_URL}"
                    f"/{self.endpoint}"
                )

                async with session.get(
                    url,
                    params=params,
                ) as response:

                    response.raise_for_status()

                    data = await response.json()

                if not data:
                    break

                for item in data:

                    record_id = item.get(
                        "id"
                    )

                    if not record_id:
                        continue

                    source_url = (
                        "https://huggingface.co/"
                        f"{self._path_prefix()}/"
                        f"{record_id}"
                    )

                    yield RawRecord(
                        source_name=self.name,
                        source_url=source_url,
                        entity_type=self.entity_type,
                        payload=item,
                        collected_at=collected_at,
                    )

                    if remaining is not None:

                        remaining -= 1

                        if remaining <= 0:
                            return

                start += len(data)

    def _path_prefix(self) -> str:

        if self.entity_type == "AI_MODEL":
            return "models"

        if self.entity_type == "DATASET":
            return "datasets"

        raise ValueError(
            f"Unsupported entity type: "
            f"{self.entity_type}"
        )