import asyncio
import logging
import aiohttp
import time

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
from src.validation.research_paper import (
    ResearchPaperValidator,
)
from src.pipeline.stats import PipelineStats
from src.pipeline.workers import bounded_map

logger = logging.getLogger(__name__)


class ResearchPaperPipeline:

    def __init__(
        self,
        enrichment_service: PaperEnrichmentService,
        batch_size: int = 10,
        concurrency: int = 5,
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
        self.validator = (
            ResearchPaperValidator()
        )

        self.batch_size = batch_size
        self.concurrency = concurrency

    async def run(
    self,
    start: int = 0,
) -> tuple[
    list[ResearchPaperEntity],
    PipelineStats,
]:

        start_time = time.perf_counter()

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

        stats = PipelineStats(
            fetched=len(raw_papers)
        )

        normalized = [
            self.normalizer.normalize(
                paper
            )
            for paper in raw_papers
        ]

        stats.normalized = len(normalized)

        processed = await bounded_map(
            normalized,
            lambda paper: self._enrich_one(
                paper,
                raw_papers,
            ),
            concurrency=self.concurrency,
        )

        results = [
            paper
            for paper in processed
            if paper is not None
        ]

        stats.enriched = len(results)
        stats.validated = len(results)

        stats.failed = (
            stats.fetched
            - stats.validated
        )

        stats.duration_seconds = (
            time.perf_counter()
            - start_time
        )

        return results, stats

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

    async def _enrich_one(
    self,
    paper: ResearchPaperEntity,
    raw_papers: list[dict],
) -> ResearchPaperEntity | None:

        try:
            abstract = self._find_abstract(
                raw_papers,
                paper.content.paper_url,
            )

            enriched = await self.enrichment.enrich(
                title=paper.content.title,
                abstract=abstract,
            )

            paper.content.summary = enriched.summary
            paper.content.topics = enriched.topics
            paper.content.application_area = (
                enriched.application_area
            )

            if enriched.github_url:
                paper.content.github_url = (
                    enriched.github_url
                )

            paper = self.validator.validate(
                paper
            )

            return paper

        except Exception as exc:
            logger.exception(
                "Paper processing failed | title=%s | error=%s",
                paper.content.title,
                exc,
            )

            return None