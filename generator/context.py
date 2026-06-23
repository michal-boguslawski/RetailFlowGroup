from pathlib import Path

from generator.core.id_generator import IdGenerator

id_generator = IdGenerator(
    config=config.ids,
    state_path=Path(f".generator_state_{store_id}.json"),
)

# generator/context.py

@classmethod
def for_store(cls, store_id: str) -> "GeneratorContext":
    config = load_config(store_id)
    builder = _BUILDERS[store_id]

    router = builder.build_router(config)
    factory = builder.build_factory(config)
    handlers = builder.build_handlers(config, factory, router)

    session_factory = SessionFactory(config, handlers)
    loop = GeneratorLoop(config, session_factory, factory.ids)

    return cls(config, router, factory, session_factory, loop)
