import asyncio

from src.crawlers.http import HTTPCrawler
from src.logging_config import configure_logging


async def main():

    configure_logging()

    crawler = HTTPCrawler(
        source_name="Example",
        concurrency=5,
    )

    await crawler.start()

    urls = [
    "https://example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
]

    try:

        results = await asyncio.gather(
            *[
                crawler.fetch(url)
                for url in urls
            ]
        )

        for result in results:

            print()
            print("SOURCE:", result.source_name)
            print("URL:", result.source_url)
            print("STATUS:", result.status_code)
            print("HASH:", result.content_hash)
            print(
                "CONTENT TYPE:",
                result.content_type
            )
            print(
                "HTML LENGTH:",
                len(result.raw_html or "")
            )

    finally:
        await crawler.close()


if __name__ == "__main__":
    asyncio.run(main())