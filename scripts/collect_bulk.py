import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline.bulk_collection import collect_bulk_data


async def main():
    print("Starting bulk collection...")

    result = await collect_bulk_data(
        startup_limit=1000,
        product_limit=1000,
        paper_limit=1000,
    )

    print()
    print("Collection complete!")
    print(f"Startups: {len(result.startups)}")
    print(f"Products: {len(result.products)}")
    print(f"Papers:   {len(result.papers)}")


if __name__ == "__main__":
    asyncio.run(main())