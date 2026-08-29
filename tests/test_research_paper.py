from src.parsers.research_papers import (
    ResearchPaperNormalizer,
)


def test_research_paper_normalization():

    paper = {
        "title": "Example AI Paper",
        "authors": [
            "Alice",
            "Bob",
        ],
        "published": (
            "2026-08-29T10:00:00Z"
        ),
        "paper_url": (
            "https://arxiv.org/abs/1234.5678"
        ),
    }

    normalizer = ResearchPaperNormalizer()

    result = normalizer.normalize(paper)

    assert (
        result.recordType
        == "RESEARCH_PAPER"
    )

    assert (
        result.content.title
        == "Example AI Paper"
    )

    assert len(
        result.content.authors
    ) == 2

    assert (
        result.content.github_url
        is None
    )