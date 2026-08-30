# src/llm/schemas.py

from pydantic import BaseModel, Field


class EnrichmentResult(BaseModel):

    summary: str = ""

    category: str | None = None

    tags: list[str] = Field(
        default_factory=list
    )

    use_cases: list[str] = Field(
        default_factory=list
    )

    application_area: str | None = None