import pytest

from src.llm.models import (
    LLMRequest,
    LLMResponse,
)
from src.llm.orchestrator import (
    LLMOrchestrator,
)
from src.llm.providers import (
    BaseLLMProvider,
)


class FakeProvider(
    BaseLLMProvider
):

    name = "fake"

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        return LLMResponse(
            provider=self.name,
            model="fake-model",
            content='{"status": "ok"}',
        )


@pytest.mark.asyncio
async def test_llm_orchestrator():

    provider = FakeProvider()

    orchestrator = LLMOrchestrator(
        providers=[provider]
    )

    request = LLMRequest(
        system_prompt="Return JSON.",
        user_prompt="Say hello.",
    )

    response = await orchestrator.generate(
        request
    )

    assert response.provider == "fake"

    assert '"status": "ok"' in (
        response.content
    )