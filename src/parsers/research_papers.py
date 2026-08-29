from datetime import datetime, timezone

from src.models.schemas import (
    ResearchPaperContent,
    ResearchPaperEntity,
)


class ResearchPaperNormalizer:

    def normalize(
        self,
        paper: dict,
    ) -> ResearchPaperEntity:

        published = datetime.fromisoformat(
            paper["published"].replace(
                "Z",
                "+00:00",
            )
        )

        if published.tzinfo is None:
            published = published.replace(
                tzinfo=timezone.utc
            )

        return ResearchPaperEntity(
            content=ResearchPaperContent(
                title=paper["title"],
                authors=paper["authors"],
                paper_url=paper["paper_url"],
                published_date=published,
            ),
            collectedAt=datetime.now(timezone.utc),
        )