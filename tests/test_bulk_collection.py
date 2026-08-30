import asyncio

from src.acquisition.models import RawRecord
from src.pipeline.bulk_collection import (
    collect_bulk_data,
)
from src.normalization.startups import (
    normalize_startup,
)
from src.normalization.products import (
    normalize_product,
)
from src.normalization.papers import (
    normalize_paper,
)


def test_normalize_startup_allows_blank_linkedin_url():
    record = RawRecord(
        source_name="example",
        source_url="https://example.com",
        canonical_url="https://example.com/startup",
        entity_type="startup",
        payload={
            "name": "Example Startup",
            "website": "https://example.com",
            "linkedin_url": "   ",
        },
        collected_at=None,
    )

    startup = normalize_startup(record)

    assert startup is not None
    assert startup.name == "Example Startup"
    assert startup.linkedin_url is None


async def main():

    result = await collect_bulk_data(
        startup_limit=1000,
        product_limit=1000,
        paper_limit=1000
    )

    print(
        f"Startups collected: "
        f"{len(result.startups)}"
    )

    print(
        f"Products collected: "
        f"{len(result.products)}"
    )

    print(
        f"Papers collected: "
        f"{len(result.papers)}"
    )

    startups = result.startups
    products = result.products
    papers = result.papers

    print("\nNORMALIZATION")

    print(
        f"Normalized startups: {len(startups)}"
    )
    print(
        f"Normalized products: {len(products)}"
    )
    print(
        f"Normalized papers: {len(papers)}"
    )

    if not startups:
        print("\nNo startups collected.")
        return

    if not products:
        print("\nNo products collected.")
        return

    if not papers:
        print("\nNo papers collected.")
        return

    print("\nSAMPLE STARTUP")
    print(startups[0].model_dump())

    print("\nSAMPLE PRODUCT")
    print(products[0].model_dump())

    print("\nSAMPLE PAPER")
    print(papers[0].model_dump())


if __name__ == "__main__":
    asyncio.run(main())