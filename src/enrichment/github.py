import logging

import aiohttp

logger = logging.getLogger(__name__)


class GitHubEnricher:

    API_BASE = "https://api.github.com"

    def __init__(
        self,
        token: str | None = None,
    ):
        self.token = token

    async def get_repository(
        self,
        session: aiohttp.ClientSession,
        owner: str,
        repo: str,
    ) -> dict | None:

        url = (
            f"{self.API_BASE}/repos/"
            f"{owner}/{repo}"
        )

        headers = {
            "Accept": (
                "application/vnd.github+json"
            )
        }

        if self.token:
            headers["Authorization"] = (
                f"Bearer {self.token}"
            )

        try:

            async with session.get(
                url,
                headers=headers,
            ) as response:

                if response.status == 404:

                    logger.info(
                        "GitHub repository not found | %s",
                        url,
                    )

                    return None

                if response.status == 403:

                    logger.warning(
                        "GitHub API access limited | %s",
                        url,
                    )

                    return None

                response.raise_for_status()

                return await response.json()

        except aiohttp.ClientError as exc:

            logger.error(
                "GitHub enrichment failed | "
                "repo=%s/%s | error=%s",
                owner,
                repo,
                exc,
            )

            return None