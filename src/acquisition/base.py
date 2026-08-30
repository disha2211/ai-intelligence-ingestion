# src/acquisition/base.py

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from src.acquisition.models import RawRecord


class AcquisitionSource(ABC):
    """
    Contract implemented by every external data source.
    """

    name: str
    entity_type: str

    @abstractmethod
    async def fetch(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> AsyncIterator[RawRecord]:
        """
        Yield raw records from the source.

        Implementations must:
        - be asynchronous
        - preserve source URLs
        - support pagination where possible
        - avoid loading the entire dataset into memory
        """
        raise NotImplementedError