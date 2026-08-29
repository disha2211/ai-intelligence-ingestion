import asyncio
import logging

from src.llm.models import (
    LLMRequest,
    LLMResponse,
)
from src.llm.providers import (
    BaseLLMProvider,
)
from src.llm.retry import (
    backoff_delay,
    is_retryable,
)


logger = logging.getLogger(__name__)


class LLMOrchestrator:

    def __init__(
        self,
        providers: list[BaseLLMProvider],
        retries_per_provider: int = 2,
    ):
        self.providers = providers
        self.retries_per_provider = (
            retries_per_provider
        )

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        last_error: Exception | None = None

        for provider in self.providers:

            logger.info(
                "Trying LLM provider | provider=%s",
                provider.name,
            )

            for attempt in range(
                self.retries_per_provider + 1
            ):

                try:

                    response = (
                        await provider.generate(
                            request
                        )
                    )

                    logger.info(
                        "LLM success | "
                        "provider=%s | "
                        "attempt=%s",
                        provider.name,
                        attempt + 1,
                    )

                    return response

                except Exception as exc:

                    last_error = exc

                    if not is_retryable(exc):

                        logger.warning(
                            "Non-retryable LLM "
                            "error | provider=%s "
                            "| error=%s",
                            provider.name,
                            exc,
                        )

                        break

                    if (
                        attempt
                        >= self.retries_per_provider
                    ):
                        logger.warning(
                            "Provider exhausted | "
                            "provider=%s",
                            provider.name,
                        )

                        break

                    delay = backoff_delay(
                        attempt
                    )

                    logger.warning(
                        "LLM retry | "
                        "provider=%s | "
                        "attempt=%s | "
                        "delay=%.2f",
                        provider.name,
                        attempt + 1,
                        delay,
                    )

                    await asyncio.sleep(
                        delay
                    )

        raise RuntimeError(
            "All LLM providers failed"
        ) from last_error