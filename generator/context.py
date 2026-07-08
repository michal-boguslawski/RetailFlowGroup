from dataclasses import dataclass
from typing import Protocol, Any

from config.loader import load_config
from config.models import OnStartBuildConfig, BreaktimeConfig, AsyncGenerationConfig
from generator.builders.base import StoreBuilder
from generator.stores.base import BaseRouter
from generator.stores.factory import StoreFactory
from generator.pipeline.builder import build_pipeline, Pipeline


class EventHandler(Protocol):
    def step(self, *args, **kwargs) -> Any: ...
    def flush(self, *args, **kwargs) -> Any: ...


@dataclass
class StoreContext:
    store_id: str
    factory: StoreFactory
    router: BaseRouter
    event_handler: EventHandler
    breaktime_config: BreaktimeConfig
    on_start_build: list[OnStartBuildConfig] | None = None
    async_generators: list[AsyncGenerationConfig] | None = None
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
            breaktime_config=config.breaktime_config,
            on_start_build=config.on_start_build,
            async_generators=config.async_generators,
            pipeline=pipeline,
        )
