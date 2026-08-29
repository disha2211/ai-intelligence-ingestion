import json
import re
from datetime import datetime, timedelta, timezone

from bs4 import BeautifulSoup


class DateParser:

    RELATIVE_PATTERNS = {
        "just now": timedelta(minutes=1),
        "a minute ago": timedelta(minutes=1),
        "an hour ago": timedelta(hours=1),
        "a day ago": timedelta(days=1),
    }

    def parse_relative(
        self,
        value: str,
        now: datetime | None = None,
    ) -> datetime | None:

        if not value:
            return None

        now = now or datetime.now(timezone.utc)

        normalized = value.strip().lower()

        if normalized in self.RELATIVE_PATTERNS:
            return (
                now
                - self.RELATIVE_PATTERNS[normalized]
            )

        match = re.match(
            r"(\d+)\s+(minute|minutes|hour|hours|day|days)\s+ago",
            normalized,
        )

        if not match:
            return None

        amount = int(match.group(1))
        unit = match.group(2)

        if "minute" in unit:
            return now - timedelta(minutes=amount)

        if "hour" in unit:
            return now - timedelta(hours=amount)

        if "day" in unit:
            return now - timedelta(days=amount)

        return None


def parse_iso(value: str) -> datetime | None:

    if not value:
        return None

    value = value.strip()

    try:
        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(
                tzinfo=timezone.utc
            )

        return parsed.astimezone(timezone.utc)

    except ValueError:
        return None


def extract_jsonld_dates(
    soup: BeautifulSoup,
) -> list[str]:

    dates = []

    scripts = soup.find_all(
        "script",
        attrs={
            "type": "application/ld+json"
        },
    )

    for script in scripts:

        raw = script.string

        if not raw:
            continue

        try:
            data = json.loads(raw)

        except json.JSONDecodeError:
            continue

        objects = (
            data
            if isinstance(data, list)
            else [data]
        )

        for obj in objects:

            if not isinstance(obj, dict):
                continue

            # Publication date gets priority.
            value = obj.get("datePublished")

            if isinstance(value, str):
                dates.append(value)

            # Keep these available for future
            # source-specific logic.
            for field in (
                "dateCreated",
                "dateModified",
            ):
                value = obj.get(field)

                if isinstance(value, str):
                    dates.append(value)

    return dates