# src/llm/base.py

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):

    name: str

    @abstractmethod
    async def generate(
        self,
        *,
        prompt: str,
        response_schema: dict[str, Any] | None = None,
    ) -> str:
        raise NotImplementedError