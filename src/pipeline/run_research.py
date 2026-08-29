from dotenv import load_dotenv

import asyncio

from src.llm.orchestrator import (
    LLMOrchestrator,
)
from src.llm.gemini import (
    GeminiProvider,
)
from src.llm.groq import (
    GroqProvider,
)
from src.llm.deepseek import (
    DeepSeekProvider,
)
from src.enrichment.paper import (
    PaperEnrichmentService,
)
from src.pipeline.research_papers import (
    ResearchPaperPipeline,
)


load_dotenv()


async def main():

    providers = []

    try:
        providers.append(
            GeminiProvider()
        )
    except ValueError:
        print(f"Gemini unavailable: {exc}")

    try:
        providers.append(
            GroqProvider()
        )
    except ValueError:
        print(f"Groq unavailable: {exc}")

    try:
        providers.append(
            DeepSeekProvider()
        )
    except ValueError:
        print(f"DeepSeek unavailable: {exc}")

    if not providers:
        raise RuntimeError(
            "No LLM providers configured"
        )

    orchestrator = LLMOrchestrator(
        providers=providers
    )

    enrichment = PaperEnrichmentService(
        llm=orchestrator
    )

    pipeline = ResearchPaperPipeline(
        enrichment_service=enrichment,
        batch_size=10,
    )

    papers, stats = await pipeline.run()

    print("\nPipeline Statistics")
    print("-" * 40)

    print(
        f"Fetched:       {stats.fetched}"
    )

    print(
        f"Normalized:    {stats.normalized}"
    )

    print(
        f"Enriched:      {stats.enriched}"
    )

    print(
        f"Validated:     {stats.validated}"
    )

    print(
        f"Failed:        {stats.failed}"
    )

    print(
        f"Success rate:  {stats.success_rate:.2f}%"
    )

    print(
        f"Duration:      {stats.duration_seconds:.2f}s"
    )

    print(
        f"Throughput:    {stats.records_per_second:.2f} records/s"
    )

    print(
        f"\nProcessed {len(papers)} papers\n"
    )

    for paper in papers:

        print("=" * 70)

        print(
            "TITLE:",
            paper.content.title
        )

        print(
            "AUTHORS:",
            ", ".join(
                paper.content.authors
            )
        )

        print(
            "TOPICS:",
            paper.content.topics
        )

        print(
            "APPLICATION:",
            paper.content.application_area
        )

        print(
            "SUMMARY:",
            paper.content.summary
        )

        print(
            "GITHUB:",
            paper.content.github_url
        )


if __name__ == "__main__":
    asyncio.run(main())