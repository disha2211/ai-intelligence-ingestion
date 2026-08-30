from src.llm.orchestrator import LLMOrchestrator
from src.models.canonical import (
    Startup,
    Product,
    ResearchPaper,
)


class EnrichmentService:

    def __init__(
        self,
        llm: LLMOrchestrator,
    ) -> None:

        self.llm = llm

    async def enrich_startup(
        self,
        startup: Startup,
    ) -> Startup:

        text = f"""
Name: {startup.name}

Description:
{startup.description}

Industry:
{startup.industry or "Unknown"}

Location:
{startup.location or "Unknown"}

Funding Stage:
{startup.funding_stage or "Unknown"}
"""

        result = await self.llm.enrich(
            text=text
        )

        # Only fill fields that are useful
        # and don't overwrite source-of-truth
        # information unnecessarily.

        if not startup.industry:
            startup.industry = result.category

        return startup

    async def enrich_product(
        self,
        product: Product,
    ) -> Product:

        text = f"""
Product Name:
{product.name}

Description:
{product.description}

Category:
{product.category or "Unknown"}

Company:
{product.company or "Unknown"}

Pricing:
{product.pricing or "Unknown"}
"""

        result = await self.llm.enrich(
            text=text
        )

        if not product.category:
            product.category = result.category

        if not product.features_use_cases:
            product.features_use_cases = (
                result.use_cases
            )

        return product

    async def enrich_paper(
        self,
        paper: ResearchPaper,
    ) -> ResearchPaper:

        text = f"""
Paper Title:
{paper.title}

Authors:
{", ".join(paper.authors)}

Abstract:
{paper.abstract}
"""

        result = await self.llm.enrich(
            text=text
        )

        # Keep the original arXiv abstract.
        # The LLM summary is additional enrichment.
        #
        # We currently don't have a separate
        # summary field in ResearchPaper, so
        # don't overwrite the source abstract.

        return paper