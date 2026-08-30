from collections.abc import AsyncIterator
from datetime import datetime, timezone
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from src.acquisition.base import AcquisitionSource
from src.acquisition.models import RawRecord


class FuturepediaSource(AcquisitionSource):
    """
    Acquires AI products from Futurepedia's public directory.

    The directory contains thousands of AI tools across
    multiple categories.
    """

    name = "futurepedia"
    entity_type = "PRODUCT"

    BASE_URL = "https://www.futurepedia.io"

    CATEGORY_URLS = [
        "/ai-tools",
        "/ai-tools/productivity",
        "/ai-tools/business",
        "/ai-tools/chatbots",
        "/ai-tools/code",
        "/ai-tools/image",
        "/ai-tools/video",
        "/ai-tools/audio",
        "/ai-tools/marketing",
        "/ai-tools/writing",
        "/ai-tools/misc-tools",
    ]

    def __init__(
        self,
        *,
        max_pages_per_category: int = 20,
    ) -> None:

        self.max_pages_per_category = (
            max_pages_per_category
        )

    async def fetch(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[RawRecord]:

        collected_at = datetime.now(
            timezone.utc
        )

        seen_urls: set[str] = set()

        collected = 0

        timeout = aiohttp.ClientTimeout(
            total=30
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; "
                "AI-Intelligence-Pipeline/1.0)"
            )
        }

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
        ) as session:

            for category in self.CATEGORY_URLS:

                for page in range(
                    1,
                    self.max_pages_per_category + 1,
                ):

                    url = self._page_url(
                        category,
                        page,
                    )

                    try:

                        async with session.get(
                            url
                        ) as response:

                            if (
                                response.status
                                == 404
                            ):
                                break

                            response.raise_for_status()

                            html = (
                                await response.text()
                            )

                    except aiohttp.ClientResponseError:
                        raise

                    soup = BeautifulSoup(
                        html,
                        "html.parser",
                    )

                    products = (
                        self._extract_products(
                            soup,
                            source_page_url=url,
                        )
                    )

                    if not products:
                        break

                    new_records = 0

                    for product in products:

                        product_url = product[
                            "url"
                        ]

                        if (
                            product_url
                            in seen_urls
                        ):
                            continue

                        seen_urls.add(
                            product_url
                        )

                        yield RawRecord(
                                source_name=self.name,
                                source_url=url,
                                canonical_url=product["url"],
                                entity_type=self.entity_type,
                                payload=product,
                                collected_at=collected_at,
                            )
                        collected += 1
                        new_records += 1

                        if (
                            limit is not None
                            and collected >= limit
                        ):
                            return

                    # If pagination produces no new
                    # records, stop this category.
                    if new_records == 0:
                        break

    def _page_url(
        self,
        category: str,
        page: int,
    ) -> str:

            if page == 1:
                return urljoin(
                    self.BASE_URL,
                    category,
                )

            return urljoin(
                self.BASE_URL,
                f"{category}?page={page}",
            )

    def _extract_products(
    self,
    soup: BeautifulSoup,
    source_page_url: str,
) -> list[dict]:

            results: list[dict] = []

            # Futurepedia's rendered directory pages contain
            # tool cards with visible "Visit" links.
            #
            # We inspect all anchors and identify candidate
            # product cards based on their surrounding content.

            for link in soup.find_all("a", href=True):

                href = link.get("href", "").strip()

                if not href:
                    continue

                # Ignore navigation / category links.
                if href.startswith("#"):
                    continue

                text = link.get_text(
                    " ",
                    strip=True,
                )

                if not text:
                    continue

                # A product card normally contains a "Visit"
                # action. Walk up the DOM to locate the card.
                if text.lower() != "visit":
                    continue

                card = link

                for _ in range(6):

                    card = card.parent

                    if card is None:
                        break

                    card_text = card.get_text(
                        " ",
                        strip=True,
                    )

                    # Product cards contain substantially more
                    # information than the Visit link itself.
                    if len(card_text) >= 50:

                        product = self._parse_card(
                            card,
                            source_link=link,
                        )

                        if product is not None:
                            results.append(product)

                        break

            return self._deduplicate(results)
    
    def _parse_card(
    self,
    card,
    source_link,
) -> dict | None:

        text = card.get_text(
            " ",
            strip=True,
        )

        if not text:
            return None

        # Find links inside the card.
        links = card.find_all(
            "a",
            href=True,
        )

        product_url = None

        for link in links:

            href = link.get(
                "href",
                "",
            ).strip()

            if not href:
                continue

            # Prefer an external destination if present.
            if href.startswith(
                "https://"
            ) or href.startswith(
                "http://"
            ):

                if "futurepedia.io" not in href:
                    product_url = href
                    break

        # If no external URL is available, retain the
        # Futurepedia page as the legitimate source URL.
        if product_url is None:

            href = source_link.get(
                "href",
                "",
            ).strip()

            if href:

                product_url = urljoin(
                    self.BASE_URL,
                    href,
                )

        if not product_url:
            return None

        name = self._extract_name(
            card
        )

        if not name:
            return None

        description = self._extract_description(
            card
        )

        return {
            "name": name,
            "description": description,
            "url": product_url,
        }



    def _extract_name(
    self,
    card,
) -> str:

        # Try headings first.
        for tag in (
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ):

            element = card.find(tag)

            if element:

                name = element.get_text(
                    " ",
                    strip=True,
                )

                if name:
                    return name

        # Fallback: inspect links other than "Visit".
        for link in card.find_all(
            "a",
            href=True,
        ):

            text = link.get_text(
                " ",
                strip=True,
            )

            if (
                text
                and text.lower() != "visit"
                and len(text) < 150
            ):
                return text

        return ""


    
    def _extract_description(
    self,
    card,
) -> str:

        paragraph = card.find("p")

        if paragraph is None:
            return ""

        return paragraph.get_text(
            " ",
            strip=True,
        )[:2000]


    @staticmethod
    def _deduplicate(
        products: list[dict],
    ) -> list[dict]:

        seen: set[str] = set()
        result: list[dict] = []

        for product in products:

            url = product["url"]

            if url in seen:
                continue

            seen.add(url)
            result.append(product)

        return result

