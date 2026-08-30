import pytest

from src.acquisition.arxiv import ArxivSource
from src.acquisition.registry import (
    SourceRegistry,
)


def test_registry():

    registry = SourceRegistry()

    source = ArxivSource()

    registry.register(source)

    assert registry.get("arxiv") is source

    research_sources = (
        registry.for_entity_type(
            "RESEARCH_PAPER"
        )
    )

    assert source in research_sources


def test_duplicate_registration():

    registry = SourceRegistry()

    registry.register(
        ArxivSource()
    )

    with pytest.raises(
        ValueError
    ):
        registry.register(
            ArxivSource()
        )