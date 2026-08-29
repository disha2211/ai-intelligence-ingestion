import asyncio

from src.crawlers.http import HTTPCrawler
from src.parsers.html import HTMLParser


async def main():

    crawler = HTTPCrawler(
        source_name="Python",
        concurrency=5,
    )

    await crawler.start()

    try:

        raw = await crawler.fetch(
            "https://www.python.org/"
        )

        print(
            "RAW:",
            len(raw.raw_html or ""),
            "characters"
        )

        parser = HTMLParser()

        clean = parser.parse(raw)

        print()
        print("TITLE:", clean.title)
        print(
            "TEXT LENGTH:",
            len(clean.text)
        )
        print(
            "PUBLISHED:",
            clean.published_at
        )

        print()
        print("CONTENT PREVIEW:")
        print(clean.text[:1000])

    finally:
        await crawler.close()


if __name__ == "__main__":
    asyncio.run(main())