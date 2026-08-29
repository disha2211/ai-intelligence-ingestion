from src.models.schemas import (
    ResearchPaperEntity,
)


class ResearchPaperValidator:

    def validate(
        self,
        paper: ResearchPaperEntity,
    ) -> ResearchPaperEntity:

        if not paper.content.title.strip():
            raise ValueError(
                "Paper title cannot be empty"
            )

        if not paper.content.authors:
            raise ValueError(
                "Paper must contain authors"
            )

        if not paper.content.paper_url:
            raise ValueError(
                "Paper URL is required"
            )

        if not paper.content.published_date:
            raise ValueError(
                "Publication date is required"
            )

        if paper.content.github_stars is not None:

            if paper.content.github_stars < 0:
                raise ValueError(
                    "GitHub stars cannot be negative"
                )

        return paper