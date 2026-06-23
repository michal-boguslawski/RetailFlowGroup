from abc import ABC, abstractmethod


class BaseSink(ABC):
    @abstractmethod
    def write(self, record) -> None: ...

    @abstractmethod
    def bulk_write(self, records: list) -> None: ...

    @abstractmethod
    def flush(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
