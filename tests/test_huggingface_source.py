import pytest

from src.acquisition.huggingface_sources import (
    huggingface_datasets,
    huggingface_models,
)


@pytest.mark.asyncio
async def test_huggingface_models():

    records = []

    async for record in huggingface_models.fetch(
        limit=5
    ):
        records.append(record)

    assert len(records) == 5

    for record in records:
        assert (
            record.source_name
            == "huggingface_models"
        )

        assert (
            record.entity_type
            == "AI_MODEL"
        )

        assert record.source_url.startswith(
            "https://huggingface.co/models/"
        )

        assert record.payload.get("id")


@pytest.mark.asyncio
async def test_huggingface_datasets():

    records = []

    async for record in huggingface_datasets.fetch(
        limit=5
    ):
        records.append(record)

    assert len(records) == 5

    for record in records:
        assert (
            record.source_name
            == "huggingface_datasets"
        )

        assert (
            record.entity_type
            == "DATASET"
        )

        assert record.source_url.startswith(
            "https://huggingface.co/datasets/"
        )

        assert record.payload.get("id")