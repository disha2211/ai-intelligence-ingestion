import asyncio
import random


RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


def get_status_code(
    exc: Exception,
) -> int | None:

    return getattr(
        exc,
        "status_code",
        None,
    )


def is_retryable(
    exc: Exception,
) -> bool:

    if isinstance(
        exc,
        asyncio.TimeoutError,
    ):
        return True

    status_code = get_status_code(exc)

    return (
        status_code
        in RETRYABLE_STATUS_CODES
    )


def backoff_delay(
    attempt: int,
    base: float = 1.0,
    maximum: float = 30.0,
) -> float:

    exponential = min(
        maximum,
        base * (2 ** attempt),
    )

    jitter = random.uniform(
        0,
        exponential * 0.25,
    )

    return exponential + jitter