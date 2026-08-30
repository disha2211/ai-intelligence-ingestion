# src/llm/orchestrator.py

import logging
from typing import Any

from src.llm.base import LLMProvider
from src.llm.chunking import chunk_text
from src.llm.retry import retry_with_backoff
from src.llm.schemas import EnrichmentResult


logger = logging.getLogger(__name__)


class LLMOrchestrator:

    def __init__(
        self,
        providers: list[LLMProvider],
    ) -> None:

        if not providers:
            raise ValueError(
                "At least one LLM provider is required"
            )

        self.providers = providers

    async def enrich(
        self,
        *,
        text: str,
    ) -> EnrichmentResult:

        chunks = chunk_text(text)

        if not chunks:
            return EnrichmentResult()

        if len(chunks) == 1:

            return await self._generate(
                chunks[0]
            )

        return await self._chunk_and_reduce(
            chunks
        )

    async def _generate(
        self,
        text: str,
    ) -> EnrichmentResult:

        last_error: Exception | None = None

        for provider in self.providers:

            try:

                logger.info(
                    "Trying LLM provider=%s",
                    provider.name,
                )

                async def operation():
                    return await provider.generate(
                        prompt=self._build_prompt(
                            text
                        )
                    )

                raw_response = await retry_with_backoff(
                    operation
                )

                return EnrichmentResult.model_validate_json(
                    raw_response
                )

            except Exception as exc:

                last_error = exc

                logger.warning(
                    "Provider failed | provider=%s | error=%s",
                    provider.name,
                    exc,
                )

                continue

        raise RuntimeError(
            "All LLM providers failed"
        ) from last_error

    async def _chunk_and_reduce(
        self,
        chunks: list[str],
    ) -> EnrichmentResult:

        partial_results: list[
            EnrichmentResult
        ] = []

        for index, chunk in enumerate(
            chunks
        ):

            logger.info(
                "Processing chunk %d/%d",
                index + 1,
                len(chunks),
            )

            result = await self._generate(
                chunk
            )

            partial_results.append(result)

        return await self._reduce(
            partial_results
        )

    async def _reduce(
        self,
        results: list[EnrichmentResult],
    ) -> EnrichmentResult:

        summaries = [
            result.summary
            for result in results
            if result.summary
        ]

        categories = [
            result.category
            for result in results
            if result.category
        ]

        tags = sorted(
            {
                tag
                for result in results
                for tag in result.tags
            }
        )

        use_cases = sorted(
            {
                use_case
                for result in results
                for use_case in result.use_cases
            }
        )

        application_areas = [
            result.application_area
            for result in results
            if result.application_area
        ]

        return EnrichmentResult(
            summary=" ".join(summaries),
            category=(
                categories[0]
                if categories
                else None
            ),
            tags=tags,
            use_cases=use_cases,
            application_area=(
                application_areas[0]
                if application_areas
                else None
            ),
        )

    @staticmethod
    def _build_prompt(
        text: str,
    ) -> str:

        return f"""
You are an information extraction system.

Extract structured metadata from the
following source content.

Return ONLY valid JSON matching:

{{
  "summary": "string",
  "category": "string or null",
  "tags": ["string"],
  "use_cases": ["string"],
  "application_area": "string or null"
}}

Do not invent information.
If a field is not supported by the source,
use null or an empty list.

SOURCE:
{text}
"""