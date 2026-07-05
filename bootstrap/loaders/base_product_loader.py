from abc import ABC, abstractmethod

from generator.core.id_generator import IdGenerator


class BaseProductSeedLoader(ABC):
    def __init__(self, id_generator: IdGenerator):
        self._id_generator = id_generator

    @abstractmethod
    def load(self, path: str) -> list:
        pass
