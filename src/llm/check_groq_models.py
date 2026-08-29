import asyncio
import os

from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

async def main():

    client = AsyncGroq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    models = await client.models.list()

    for model in models.data:
        print(model.id)


if __name__ == "__main__":
    asyncio.run(main())