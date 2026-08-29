import os

from google import genai

from src.llm.models import (
    LLMRequest,
    LLMResponse,
)
from src.llm.providers import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    name = "gemini"

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
    ):
        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured"
            )

        self.model = model

        self.client = genai.Client(
            api_key=api_key
        )

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        prompt = (
            f"{request.system_prompt}\n\n"
            f"{request.user_prompt}"
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return LLMResponse(
            provider=self.name,
            model=self.model,
            content=response.text,
        )