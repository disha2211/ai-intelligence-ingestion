import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline.bulk_collection import collect_bulk_data

from src.quality.dedup import deduplicate
from src.export.csv_export import export_csv


async def main():

    print("Collecting source data...")

    result = await collect_bulk_data(
        startup_limit=1000,
        product_limit=1000,
        paper_limit=1000,
    )

    print(
        f"Raw records -> "
        f"startups={len(result.startups)}, "
        f"products={len(result.products)}, "
        f"papers={len(result.papers)}"
    )

    print("Normalizing...")

    startups = list(result.startups)
    products = list(result.products)
    papers = list(result.papers)

    print("Deduplicating...")

    startups = deduplicate(startups)
    products = deduplicate(products)
    papers = deduplicate(papers)

    print(
        f"Final records -> "
        f"startups={len(startups)}, "
        f"products={len(products)}, "
        f"papers={len(papers)}"
    )

    print("Exporting CSV files...")

    export_csv(
        startups,
        "output/startups.csv",
    )

    export_csv(
        products,
        "output/products.csv",
    )

    export_csv(
        papers,
        "output/research_papers.csv",
    )

    print()
    print("DONE")
    print("output/startups.csv")
    print("output/products.csv")
    print("output/research_papers.csv")


if __name__ == "__main__":
    asyncio.run(main())