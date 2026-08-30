# src/acquisition/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RawRecord:
    """
    Source-level record.

    This represents data exactly as obtained from an external
    source before canonical normalization/enrichment.
    """

    source_name: str
    source_url: str
    canonical_url: str | None
    entity_type: str
    payload: dict[str, Any]
    collected_at: datetime