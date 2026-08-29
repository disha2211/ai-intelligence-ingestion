import json

from src.llm.models import LLMRequest
from src.llm.orchestrator import LLMOrchestrator
from src.llm.structured import parse_structured_output
from src.models.schemas import PaperEnrichment


class PaperEnrichmentService:

    def __init__(
        self,
        llm: LLMOrchestrator,
    ):
        self.llm = llm

    async def enrich(
        self,
        title: str,
        abstract: str,
    ) -> PaperEnrichment:

        system_prompt = """
You are an AI research metadata extraction system.

Analyze the research paper information provided by the user.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{
  "summary": "concise summary",
  "topics": ["topic1", "topic2"],
  "application_area": "string or null",
  "github_url": "URL or null"
}

Do not invent a GitHub repository.
If no repository is explicitly supported by the provided information,
return null.
"""

        user_prompt = f"""
Paper title:
{title}

Abstract:
{abstract}
"""

        request = LLMRequest(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.0,
            max_tokens=1000,
        )

        response = await self.llm.generate(
            request
        )

        return parse_structured_output(
            response.content,
            PaperEnrichment,
        )