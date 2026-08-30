from src.models.schemas import (
    ResearchPaperEntity,
)


def research_paper_to_entity(
    paper: ResearchPaperEntity,
) -> dict:

    content = paper.content

    metadata = {
        "authors": content.authors,
        "github_url": (
            str(content.github_url)
            if content.github_url
            else None
        ),
        "github_stars": content.github_stars,
        "published_date": (
            content.published_date.isoformat()
        ),
        "topics": content.topics,
        "application_area": (
            content.application_area
        ),
    }

    return {
        "entity_type": "RESEARCH_PAPER",
        "name": content.title,
        "description": content.summary,
        "url": str(content.paper_url),
        "source": "arXiv",
        "metadata": metadata,
    }