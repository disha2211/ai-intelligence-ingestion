# src/acquisition/arxiv.py
import ssl

import certifi

from collections.abc import AsyncIterator
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

import aiohttp

from src.acquisition.base import AcquisitionSource
from src.acquisition.models import RawRecord


class ArxivSource(AcquisitionSource):

    name = "arxiv"
    entity_type = "RESEARCH_PAPER"

    API_URL = (
        "https://export.arxiv.org/api/query"
    )

    PAGE_SIZE = 100

    NS = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    async def fetch(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[RawRecord]:

        start = int(cursor or 0)

        remaining = limit

        timeout = aiohttp.ClientTimeout(
            total=60
        )

        headers = {
            "User-Agent": (
                "AI-Intelligence-Pipeline/1.0 "
                "(research assignment)"
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

                batch_size = self.PAGE_SIZE

                if remaining is not None:
                    batch_size = min(
                        batch_size,
                        remaining,
                    )

                params = {
                    "search_query": (
                        "cat:cs.AI OR "
                        "cat:cs.LG OR "
                        "cat:cs.CL"
                    ),
                    "start": start,
                    "max_results": batch_size,
                    "sortBy": "submittedDate",
                    "sortOrder": "descending",
                }

                ssl_context = ssl.create_default_context(
                            cafile=certifi.where()
                        )

                async with session.get(
                    self.API_URL,
                    params=params,
                    ssl=ssl_context,
                ) as response:

                    response.raise_for_status()

                    xml_text = await response.text()

                records = self._parse_response(
                    xml_text
                )

                if not records:
                    break

                for record in records:

                    yield record

                    if remaining is not None:

                        remaining -= 1

                        if remaining <= 0:
                            return

                start += len(records)

    def _parse_response(
        self,
        xml_text: str,
    ) -> list[RawRecord]:

        root = ElementTree.fromstring(
            xml_text
        )

        collected_at = datetime.now(
            timezone.utc
        )

        records: list[RawRecord] = []

        for entry in root.findall(
            "atom:entry",
            self.NS,
        ):

            title = self._text(
                entry,
                "atom:title",
            )

            summary = self._text(
                entry,
                "atom:summary",
            )

            paper_url = self._extract_url(
                entry
            )

            published_raw = self._text(
                entry,
                "atom:published",
            )

            authors = [
                self._text(
                    author,
                    "atom:name",
                )
                for author in entry.findall(
                    "atom:author",
                    self.NS,
                )
            ]

            payload = {
                "title": title,
                "summary": summary,
                "authors": authors,
                "paper_url": paper_url,
                "published": published_raw,
            }

            records.append(
                RawRecord(
                source_name=self.name,
                source_url=self.API_URL,
                canonical_url=paper_url,
                entity_type=self.entity_type,
                payload=payload,
                collected_at=collected_at,
            )
            )

        return records

    @staticmethod
    def _text(
        element,
        path: str,
    ) -> str:

        child = element.find(
            path,
            {
                "atom": (
                    "http://www.w3.org/2005/Atom"
                )
            },
        )

        if child is None or child.text is None:
            return ""

        return " ".join(
            child.text.split()
        )

    def _extract_url(
        self,
        entry,
    ) -> str:

        for link in entry.findall(
            "atom:link",
            self.NS,
        ):

            if (
                link.attrib.get("rel")
                == "alternate"
            ):
                href = link.attrib.get(
                    "href"
                )

                if href:
                    return href

        raise ValueError(
            "arXiv entry has no alternate URL"
        )