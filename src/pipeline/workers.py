import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


async def bounded_map(
    items: list[T],
    worker: Callable[[T], Awaitable[R]],
    concurrency: int = 5,
) -> list[R]:

    semaphore = asyncio.Semaphore(
        concurrency
    )

    async def run_one(item: T) -> R:
        async with semaphore:
            return await worker(item)

    tasks = [
        asyncio.create_task(
            run_one(item)
        )
        for item in items
    ]

    return await asyncio.gather(
        *tasks
    )