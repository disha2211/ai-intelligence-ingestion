import os

from groq import AsyncGroq

from src.llm.models import (
    LLMRequest,
    LLMResponse,
)
from src.llm.providers import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    name = "groq"

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
    ):
        api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured"
            )

        self.model = model

        self.client = AsyncGroq(
            api_key=api_key
        )

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": request.system_prompt,
                },
                {
                    "role": "user",
                    "content": request.user_prompt,
                },
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        message = response.choices[0].message

        return LLMResponse(
            provider=self.name,
            model=self.model,
            content=message.content or "",
            input_tokens=getattr(
                response.usage,
                "prompt_tokens",
                None,
            ),
            output_tokens=getattr(
                response.usage,
                "completion_tokens",
                None,
            ),
        )