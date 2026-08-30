import pytest

from src.acquisition.arxiv import ArxivSource


@pytest.mark.asyncio
async def test_arxiv_source():

    source = ArxivSource()

    records = []

    async for record in source.fetch(
        limit=5
    ):
        records.append(record)

    assert len(records) == 5

    for record in records:

        assert (
            record.source_name
            == "arxiv"
        )

        assert (
            record.entity_type
            == "RESEARCH_PAPER"
        )

        assert record.source_url.startswith(
            "http"
        )

        assert record.payload["title"]
        assert record.payload["authors"]
        assert record.payload["published"]