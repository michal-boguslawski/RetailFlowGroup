# generator/builders/base.py

from typing import Protocol
from config.models import StoreConfig
from domain.types import BaseFactory  # generic Protocol, not the old class
from generator.session.handlers.base import TransitionHandler


class StoreBuilder(Protocol):
    def build_router(self, config: StoreConfig) -> "BaseRouter": ...
    def build_factory(self, config: StoreConfig) -> "BaseFactory": ...
    def build_handlers(self, config: StoreConfig, factory, pipeline, router) -> list[TransitionHandler]: ...
