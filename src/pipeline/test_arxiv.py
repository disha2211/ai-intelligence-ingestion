import asyncio

import aiohttp

from src.crawlers.arxiv import ArxivCrawler


async def main():

    crawler = ArxivCrawler(
        batch_size=10
    )

    timeout = aiohttp.ClientTimeout(
        total=30
    )

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        papers = await crawler.fetch_batch(
            session,
            start=0,
        )

        print(
            f"Fetched {len(papers)} papers"
        )

        for paper in papers[:3]:

            print()
            print(
                "TITLE:",
                paper["title"]
            )

            print(
                "AUTHORS:",
                paper["authors"]
            )

            print(
                "URL:",
                paper["paper_url"]
            )

            print(
                "PUBLISHED:",
                paper["published"]
            )


if __name__ == "__main__":
    asyncio.run(main())