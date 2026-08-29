import asyncio

import pytest

from src.pipeline.workers import bounded_map


@pytest.mark.asyncio
async def test_bounded_map():

    active = 0
    maximum_active = 0

    async def worker(
        value: int,
    ) -> int:

        nonlocal active
        nonlocal maximum_active

        active += 1

        maximum_active = max(
            maximum_active,
            active,
        )

        await asyncio.sleep(0.05)

        active -= 1

        return value * 2

    result = await bounded_map(
        list(range(20)),
        worker,
        concurrency=3,
    )

    assert result == [
        i * 2
        for i in range(20)
    ]

    assert maximum_active <= 3