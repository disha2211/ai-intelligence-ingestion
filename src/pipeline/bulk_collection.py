from dataclasses import dataclass

from src.acquisition.arxiv import ArxivSource
from src.acquisition.futurepedia import (
    FuturepediaSource,
)
from src.acquisition.yc import YCStartupSource
from src.acquisition.base import AcquisitionSource
from src.acquisition.models import RawRecord

from src.normalization.startups import (
    normalize_startup,
)
from src.normalization.products import (
    normalize_product,
)
from src.normalization.papers import (
    normalize_paper,
)


@dataclass
class CollectionResult:
    startups: list[RawRecord]
    products: list[RawRecord]
    papers: list[RawRecord]


async def collect_bulk_data(
    *,
    startup_limit: int = 1000,
    product_limit: int = 1000,
    paper_limit: int = 1000,
) -> CollectionResult:

    startup_source = YCStartupSource()

    product_source = FuturepediaSource(
        max_pages_per_category=20
    )

    paper_source = ArxivSource()

    startups = await collect_source(
        startup_source,
        limit=1000,
    normalizer=normalize_startup,
    )

    products = await collect_source(
        product_source,
        limit=1000,
    normalizer=normalize_product,
    )

    papers = await collect_source(
        paper_source,
        limit=1000,
    normalizer=normalize_paper,   
    )

    return CollectionResult(
        startups=startups,
        products=products,
        papers=papers,
    )


async def collect_source(
    source: AcquisitionSource,
    limit: int,
    normalizer=None,
) -> list:

    records = []

    async for record in source.fetch():

        if normalizer is not None:

            normalized = normalizer(record)

            if normalized is None:
                continue

            records.append(normalized)

        else:
            records.append(record)

        if len(records) >= limit:
            break

    return records