from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.types import GeneratedRecord
from sinks.base import BaseSink


T = TypeVar("T")


class BaseRouter(ABC):

    @abstractmethod
    def route(self, record: GeneratedRecord) -> tuple[BaseSink, ...]:
        pass


class BaseFactory(ABC, Generic[T]):

    @abstractmethod
    def make_one(self, *args, **kwargs) -> T:
        pass

    def make(self, n: int) -> list[T]:
        return [self.make_one() for _ in range(n)]
