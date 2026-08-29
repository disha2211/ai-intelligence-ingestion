from pydantic import BaseModel


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str

    temperature: float = 0.0
    max_tokens: int = 2000


class LLMResponse(BaseModel):
    provider: str
    model: str

    content: str

    input_tokens: int | None = None
    output_tokens: int | None = None