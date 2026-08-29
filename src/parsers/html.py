import re
from bs4 import BeautifulSoup

from src.models.schemas import RawDocument, CleanDocument
from src.parsers.dates import (
    parse_iso,
    extract_jsonld_dates,
)


class HTMLParser:

    REMOVE_TAGS = {
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "canvas",
    }

    def parse(self, document: RawDocument) -> CleanDocument:

        html = document.raw_html or ""

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        title = self._extract_title(soup)
        description = self._extract_description(soup)
        published_at = self._extract_published_date(soup)

        # Remove non-content elements
        for tag in soup.find_all(self.REMOVE_TAGS):
            tag.decompose()

        

        text = self._extract_text(soup)

        return CleanDocument(
            source_name=document.source_name,
            source_url=document.source_url,
            fetched_at=document.fetched_at,
            title=title,
            description=description,
            text=text,
            published_at=published_at,
            content_hash=document.content_hash,
        )

    @staticmethod
    def _extract_title(
        soup: BeautifulSoup,
    ) -> str | None:

        if soup.title:
            title = soup.title.get_text(
                " ",
                strip=True,
            )

            if title:
                return title

        return None

    @staticmethod
    def _extract_description(
        soup: BeautifulSoup,
    ) -> str | None:

        meta = soup.find(
            "meta",
            attrs={"name": "description"},
        )

        if meta and meta.get("content"):
            return meta["content"].strip()

        return None

    @staticmethod
    def _extract_text(
        soup: BeautifulSoup,
    ) -> str:

        # Remove obvious navigation/boilerplate areas.
        for tag in soup.find_all(
            ["nav", "footer", "header", "aside"]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        # Normalize excessive whitespace.
        lines = []

        for line in text.splitlines():

            line = re.sub(
                r"\s+",
                " ",
                line,
            ).strip()

            if line:
                lines.append(line)

        return "\n".join(lines)

    def _extract_published_date(
    self,
    soup: BeautifulSoup,
):

        jsonld_dates = extract_jsonld_dates(soup)

        for value in jsonld_dates:

            parsed = parse_iso(value)

            if parsed:
                return parsed

        # <time datetime="...">
        time_tags = soup.find_all("time")

        for tag in time_tags:

            value = tag.get("datetime")

            if not value:
                continue

            parsed = parse_iso(value)

            if parsed:
                return parsed

        return None