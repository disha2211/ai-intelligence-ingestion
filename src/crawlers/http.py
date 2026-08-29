import asyncio
import hashlib
import logging
import random
from datetime import datetime, timezone

import aiohttp

from src.models.schemas import RawDocument
from src.crawlers.base import BaseCrawler


logger = logging.getLogger(__name__)


class HTTPCrawler(BaseCrawler):

    def __init__(
        self,
        source_name: str,
        concurrency: int = 20,
        timeout_seconds: int = 30,
        max_retries: int = 3,
    ):
        self.source_name = source_name

        self.semaphore = asyncio.Semaphore(
            concurrency
        )

        self.timeout = aiohttp.ClientTimeout(
            total=timeout_seconds
        )

        self.max_retries = max_retries

        self.session: aiohttp.ClientSession | None = None

    async def start(self):

        if self.session is not None:
            return

        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
        )

        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout,
            headers={
                "User-Agent": (
                    "AI-Intelligence-Ingestion/1.0 "
                    "(research crawler)"
                )
            },
        )

    async def close(self):

        if self.session is not None:
            await self.session.close()
            self.session = None

    async def fetch(self, url: str) -> RawDocument:

        if self.session is None:
            raise RuntimeError(
                "Crawler has not been started. "
                "Call await crawler.start()."
            )

        async with self.semaphore:

            for attempt in range(
                self.max_retries + 1
            ):

                try:

                    async with self.session.get(
                        url,
                        allow_redirects=True,
                    ) as response:

                        body = await response.text(
                            errors="replace"
                        )

                        content_hash = hashlib.sha256(
                            body.encode("utf-8")
                        ).hexdigest()

                        logger.info(
                            "Fetched | status=%s | url=%s",
                            response.status,
                            url,
                        )

                        return RawDocument(
                            source_name=self.source_name,
                            source_url=str(response.url),
                            fetched_at=(
                                datetime.now(timezone.utc)
                            ),
                            status_code=response.status,
                            content_type=(
                                response.headers.get(
                                    "Content-Type"
                                )
                            ),
                            raw_html=body,
                            content_hash=content_hash,
                        )

                    if response.status in RETRYABLE_STATUS_CODES:

                        if attempt >= self.max_retries:
                            logger.error(
                                "Retryable HTTP status exhausted | "
                                "status=%s | url=%s",
                                response.status,
                                url,
                            )

                            return RawDocument(
                                source_name=self.source_name,
                                source_url=str(response.url),
                                fetched_at=datetime.now(timezone.utc),
                                status_code=response.status,
                                content_type=response.headers.get(
                                    "Content-Type"
                                ),
                                raw_html=body,
                                content_hash=content_hash,
                            )

                        retry_after = response.headers.get(
                            "Retry-After"
                        )

                        if retry_after:
                            try:
                                delay = float(retry_after)
                            except ValueError:
                                delay = (2 ** attempt) + random.uniform(0, 1)
                        else:
                            delay = (2 ** attempt) + random.uniform(0, 1)

                        logger.warning(
                            "Retryable HTTP status | "
                            "status=%s | delay=%s | url=%s",
                            response.status,
                            delay,
                            url,
                        )

                        await asyncio.sleep(delay)
                        continue

                except (
                    aiohttp.ClientError,
                    asyncio.TimeoutError,
                ) as exc:

                    if attempt >= self.max_retries:
                        logger.error(
                            "Request permanently failed | "
                            "url=%s | error=%s",
                            url,
                            exc,
                        )
                        raise

                    delay = (2 ** attempt) + random.uniform(0, 1)

                    logger.warning(
                        "Request failed | "
                        "attempt=%s/%s | "
                        "retrying_in=%ss | "
                        "url=%s",
                        attempt + 1,
                        self.max_retries,
                        delay,
                        url,
                    )

                    await asyncio.sleep(delay)

            raise RuntimeError("Unreachable")