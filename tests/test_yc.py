
import pytest

from src.acquisition.yc import (
    YCStartupSource,
)


@pytest.mark.asyncio
async def test_yc_startups():

    source = YCStartupSource()

    records = []

    async for record in source.fetch(
        limit=1000
    ):
        records.append(record)

    assert len(records) == 1000

    for record in records:

        assert (
            record.entity_type
            == "STARTUP"
        )

        assert record.payload

        assert record.source_url.startswith(
            "http"
        )