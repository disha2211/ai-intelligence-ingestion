# src/acquisition/runner.py

import logging
from collections.abc import AsyncIterator

from src.acquisition.base import AcquisitionSource
from src.acquisition.models import RawRecord

logger = logging.getLogger(__name__)


class AcquisitionRunner:

    async def run(
        self,
        source: AcquisitionSource,
        *,
        limit: int | None = None,
    ) -> AsyncIterator[RawRecord]:

        count = 0

        logger.info(
            "Starting acquisition | source=%s | limit=%s",
            source.name,
            limit,
        )

        try:

            async for record in source.fetch(
                limit=limit
            ):

                yield record

                count += 1

                if (
                    limit is not None
                    and count >= limit
                ):
                    break

        except Exception:

            logger.exception(
                "Acquisition failed | source=%s",
                source.name,
            )

            raise

        finally:

            logger.info(
                "Acquisition completed | source=%s | records=%d",
                source.name,
                count,
            )