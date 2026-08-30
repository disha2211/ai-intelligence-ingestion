import pytest

from src.acquisition.futurepedia import (
    FuturepediaSource,
)


@pytest.mark.asyncio
async def test_futurepedia():

    source = FuturepediaSource(
        max_pages_per_category=1
    )

    records = []

    async for record in source.fetch(
        limit=20
    ):
        print(
        record.payload["name"],
        record.source_url,
    )
        records.append(record)

    assert len(records) > 0

    for record in records:

        assert record.entity_type == "PRODUCT"

        assert record.source_name == (
            "futurepedia"
        )

        assert record.source_url.startswith(
            "https://www.futurepedia.io/"
        )

        assert record.canonical_url is not None

        assert record.canonical_url.startswith(
            "http"
        )

        assert record.payload["name"]