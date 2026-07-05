from dataclasses import dataclass
from typing import Protocol, Any

from config.loader import load_config
from generator.builders.base import StoreBuilder
from generator.stores.base import BaseRouter
from generator.stores.factory import StoreFactory
from generator.pipeline.builder import build_pipeline, Pipeline


class EventHandler(Protocol):
    def step(self) -> Any: ...


@dataclass
class StoreContext:
    store_id: str
    factory: StoreFactory
    router: BaseRouter
    event_handler: EventHandler
    async_generators: list[str] | None = None
    pipeline: Pipeline | None = None

    @classmethod
    def build(cls, builder: StoreBuilder, store_id: str) -> "StoreContext":
        config = load_config(store_id)

        pipeline = build_pipeline(config.pipeline_config) if config.pipeline_config else None

        return cls(
            store_id=store_id,
            factory=builder.build_factory(config),
            router=builder.build_router(config),
            event_handler=builder.build_handler(config),
            async_generators=config.async_generators,
            pipeline=pipeline,
        )
