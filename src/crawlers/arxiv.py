import asyncio
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import aiohttp

logger = logging.getLogger(__name__)


class ArxivCrawler:

    API_URL = "https://export.arxiv.org/api/query"

    def __init__(
        self,
        batch_size: int = 100,
        max_retries: int = 3,
    ):
        self.batch_size = batch_size
        self.max_retries = max_retries

    async def fetch_batch(
        self,
        session: aiohttp.ClientSession,
        start: int = 0,
    ) -> list[dict]:

        params = {
            "search_query": "cat:cs.AI",
            "start": start,
            "max_results": self.batch_size,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        for attempt in range(self.max_retries + 1):

            try:

                async with session.get(
                    self.API_URL,
                    params=params,
                ) as response:

                    if response.status == 429:

                        if attempt >= self.max_retries:
                            raise RuntimeError(
                                "arXiv rate limit exhausted"
                            )

                        await asyncio.sleep(
                            2 ** attempt
                        )
                        continue

                    response.raise_for_status()

                    xml = await response.text()

                    return self._parse_feed(xml)

            except (
                aiohttp.ClientError,
                asyncio.TimeoutError,
            ) as exc:

                if attempt >= self.max_retries:
                    raise

                delay = 2 ** attempt

                logger.warning(
                    "arXiv request failed | "
                    "attempt=%s | retry_in=%ss | error=%s",
                    attempt + 1,
                    delay,
                    exc,
                )

                await asyncio.sleep(delay)

        raise RuntimeError("Unexpected arXiv failure")

    def _parse_feed(
        self,
        xml: str,
    ) -> list[dict]:

        root = ET.fromstring(xml)

        namespace = {
            "atom": "http://www.w3.org/2005/Atom"
        }

        papers = []

        for entry in root.findall(
            "atom:entry",
            namespace,
        ):

            title = entry.findtext(
                "atom:title",
                default="",
                namespaces=namespace,
            ).strip()

            summary = entry.findtext(
                "atom:summary",
                default="",
                namespaces=namespace,
            ).strip()

            published = entry.findtext(
                "atom:published",
                default="",
                namespaces=namespace,
            ).strip()

            paper_id = entry.findtext(
                "atom:id",
                default="",
                namespaces=namespace,
            ).strip()
            paper_id = paper_id.replace(
                "http://",
                "https://",
            )

            authors = []

            for author in entry.findall(
                "atom:author",
                namespace,
            ):

                name = author.findtext(
                    "atom:name",
                    default="",
                    namespaces=namespace,
                )

                if name:
                    authors.append(name.strip())

            papers.append(
                {
                    "title": title,
                    "summary": summary,
                    "published": published,
                    "paper_url": paper_id,
                    "authors": authors,
                    "collected_at": datetime.now(
                        timezone.utc
                    ),
                }
            )

        return papers