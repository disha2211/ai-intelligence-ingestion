import os

from openai import AsyncOpenAI

from src.llm.models import (
    LLMRequest,
    LLMResponse,
)
from src.llm.providers import BaseLLMProvider


class DeepSeekProvider(BaseLLMProvider):

    name = "deepseek"

    def __init__(
        self,
        model: str = "deepseek-chat",
    ):
        api_key = os.getenv(
            "DEEPSEEK_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY is not configured"
            )

        self.model = model

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
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