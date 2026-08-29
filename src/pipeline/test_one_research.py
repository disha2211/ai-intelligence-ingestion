import asyncio

from src.enrichment.paper import PaperEnrichmentService
from src.llm.deepseek import DeepSeekProvider
from src.llm.gemini import GeminiProvider
from src.llm.groq import GroqProvider
from src.llm.models import LLMRequest
from src.llm.orchestrator import LLMOrchestrator
from dotenv import load_dotenv
load_dotenv()


async def main():

    providers = []

    try:
        providers.append(
            GeminiProvider()
        )
    except ValueError:
        pass

    try:
        providers.append(
            GroqProvider()
        )
    except ValueError:
        pass

    try:
        providers.append(
            DeepSeekProvider()
        )
    except ValueError:
        pass

    orchestrator = LLMOrchestrator(
        providers=providers
    )

    request = LLMRequest(
        system_prompt=(
            "Return ONLY valid JSON with "
            "one field called 'message'."
        ),
        user_prompt=(
            "Return a message saying hello "
            "from the AI ingestion pipeline."
        ),
        temperature=0.0,
        max_tokens=100,
    )

    response = await orchestrator.generate(
        request
    )

    print("\nSUCCESS")
    print("Provider:", response.provider)
    print("Model:", response.model)
    print("Response:", response.content)


if __name__ == "__main__":
    asyncio.run(main())