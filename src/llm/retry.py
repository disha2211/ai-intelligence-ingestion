# src/llm/retry.py

import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar


T = TypeVar("T")


RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


class RetryableLLMError(Exception):

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code


async def retry_with_backoff(
    operation: Callable[[], Awaitable[T]],
    *,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> T:

    attempt = 0

    while True:

        try:
            return await operation()

        except RetryableLLMError:

            if attempt >= max_retries:
                raise

            delay = min(
                max_delay,
                base_delay * (2 ** attempt),
            )

            # Jitter prevents synchronized retries.
            delay += random.uniform(
                0,
                delay * 0.25,
            )

            await asyncio.sleep(delay)

            attempt += 1