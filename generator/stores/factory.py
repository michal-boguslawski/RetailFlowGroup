from domain.types import GeneratedRecord
from generator.stores.base import BaseFactory


class StoreFactory:
    def __init__(
        self,
        factories: dict[str, BaseFactory]
    ):
        self.factories = factories

    def make_one(self, entity_name: str, *args, **kwargs) -> GeneratedRecord:
        factory = self.factories[entity_name]
        return factory.make_one(*args, **kwargs)
