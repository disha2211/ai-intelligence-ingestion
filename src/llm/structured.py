import json

from pydantic import BaseModel


def parse_structured_output(
    content: str,
    schema: type[BaseModel],
) -> BaseModel:

    cleaned = content.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix(
            "```json"
        )
        cleaned = cleaned.removeprefix(
            "```"
        )
        cleaned = cleaned.removesuffix(
            "```"
        )
        cleaned = cleaned.strip()

    data = json.loads(cleaned)

    return schema.model_validate(data)