from abc import ABC, abstractmethod

from src.models.schemas import RawDocument


class BaseCrawler(ABC):

    @abstractmethod
    async def fetch(self, url: str) -> RawDocument:
        """
        Fetch a source and return a provenance-preserving
        raw document.
        """
        raise NotImplementedError