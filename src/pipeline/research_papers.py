import asyncio
import logging

import aiohttp

from src.crawlers.arxiv import ArxivCrawler
from src.enrichment.paper import (
    PaperEnrichmentService,
)
from src.models.schemas import (
    ResearchPaperEntity,
)
from src.parsers.research_papers import (
    ResearchPaperNormalizer,
)

logger = logging.getLogger(__name__)


class ResearchPaperPipeline:

    def __init__(
        self,
        enrichment_service: PaperEnrichmentService,
        batch_size: int = 10,
    ):
        self.arxiv = ArxivCrawler(
            batch_size=batch_size
        )

        self.normalizer = (
            ResearchPaperNormalizer()
        )

        self.enrichment = (
            enrichment_service
        )

        self.batch_size = batch_size

    async def run(
        self,
        start: int = 0,
    ) -> list[ResearchPaperEntity]:

        timeout = aiohttp.ClientTimeout(
            total=60
        )

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            raw_papers = (
                await self.arxiv.fetch_batch(
                    session,
                    start=start,
                )
            )

        normalized = [
            self.normalizer.normalize(
                paper
            )
            for paper in raw_papers
        ]

        results = []

        for paper in normalized:

            try:

                enriched = (
                    await self.enrichment.enrich(
                        title=paper.content.title,
                        abstract=(
                            self._find_abstract(
                                raw_papers,
                                paper.content.paper_url,
                            )
                        ),
                    )
                )

                paper.content.summary = (
                    enriched.summary
                )

                paper.content.topics = (
                    enriched.topics
                )

                paper.content.application_area = (
                    enriched.application_area
                )

                if enriched.github_url:
                    paper.content.github_url = (
                        enriched.github_url
                    )

                results.append(paper)

            except Exception as exc:

                logger.error(
                    "Paper enrichment failed | "
                    "title=%s | error=%s",
                    paper.content.title,
                    exc,
                )

        return results

    @staticmethod
    def _find_abstract(
        raw_papers: list[dict],
        paper_url: str,
    ) -> str:

        for paper in raw_papers:

            if paper["paper_url"] == str(
                paper_url
            ):
                return paper["summary"]

        return ""