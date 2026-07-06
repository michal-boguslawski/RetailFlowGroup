from abc import ABC, abstractmethod
from domain.types import GeneratedRecord


class BaseSink(ABC):
    @abstractmethod
    def write(self, record: GeneratedRecord) -> None: ...

    @abstractmethod
    def bulk_write(self, records: list[GeneratedRecord]) -> None: ...

    @abstractmethod
    def flush(self, *args, **kwargs) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
