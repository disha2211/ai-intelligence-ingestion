from abc import ABC, abstractmethod

from src.llm.models import (
    LLMRequest,
    LLMResponse,
)


class BaseLLMProvider(ABC):

    name: str

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        raise NotImplementedError