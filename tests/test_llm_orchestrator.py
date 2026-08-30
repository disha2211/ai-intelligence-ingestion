import pytest

from src.llm.base import LLMProvider
from src.llm.orchestrator import (
    LLMOrchestrator,
)


class FailingProvider(LLMProvider):

    name = "gemini"

    async def generate(
        self,
        *,
        prompt: str,
        response_schema=None,
    ) -> str:

        raise RuntimeError(
            "simulated failure"
        )


class WorkingProvider(LLMProvider):

    name = "groq"

    async def generate(
        self,
        *,
        prompt: str,
        response_schema=None,
    ) -> str:

        return """
        {
          "summary": "Test summary",
          "category": "AI",
          "tags": ["test"],
          "use_cases": ["testing"],
          "application_area": "software"
        }
        """


@pytest.mark.asyncio
async def test_provider_fallback():

    orchestrator = LLMOrchestrator(
        providers=[
            FailingProvider(),
            WorkingProvider(),
        ]
    )

    result = await orchestrator.enrich(
        text="This is test content."
    )

    assert result.summary == (
        "Test summary"
    )

    assert result.category == "AI"

    assert "test" in result.tags