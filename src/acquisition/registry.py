# src/acquisition/registry.py

from src.acquisition.base import AcquisitionSource


class SourceRegistry:

    def __init__(self) -> None:
        self._sources: dict[str, AcquisitionSource] = {}

    def register(
        self,
        source: AcquisitionSource,
    ) -> None:

        if source.name in self._sources:
            raise ValueError(
                f"Source already registered: {source.name}"
            )

        self._sources[source.name] = source

    def get(
        self,
        name: str,
    ) -> AcquisitionSource:

        try:
            return self._sources[name]
        except KeyError:
            raise KeyError(
                f"Unknown source: {name}"
            ) from None

    def all(
        self,
    ) -> list[AcquisitionSource]:

        return list(self._sources.values())

    def for_entity_type(
        self,
        entity_type: str,
    ) -> list[AcquisitionSource]:

        return [
            source
            for source in self._sources.values()
            if source.entity_type == entity_type
        ]