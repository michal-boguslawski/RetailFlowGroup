# generator/builders/base.py

from typing import Protocol
from config.models import StoreConfig
from generator.stores.factory import StoreFactory
from generator.stores.base import BaseFactory, BaseRouter
from generator.session.machine import StateMachine


class StoreBuilder(Protocol):
    def build_router(self, config: StoreConfig) -> BaseRouter: ...
    def build_factory(self, config: StoreConfig) -> StoreFactory: ...
    def build_handler(self, config: StoreConfig) -> StateMachine: ...
