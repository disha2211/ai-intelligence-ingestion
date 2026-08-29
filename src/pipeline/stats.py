from dataclasses import dataclass
import time


@dataclass
class PipelineStats:
    fetched: int = 0
    normalized: int = 0
    enriched: int = 0
    validated: int = 0
    failed: int = 0
    duration_seconds: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.fetched == 0:
            return 0.0

        return (
            self.validated / self.fetched
        ) * 100

    @property
    def records_per_second(self) -> float:
        if self.duration_seconds <= 0:
            return 0.0

        return (
            self.validated
            / self.duration_seconds
        )