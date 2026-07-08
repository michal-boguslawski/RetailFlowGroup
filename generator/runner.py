import argparse
from datetime import date
from numpy.random import gamma
from threading import Thread

from generator.builders.registry import BUILDERS
from generator.context import StoreContext
from generator.core.loop import GeneratorLoop
from generator.session.handlers.loader import load_handlers


def run_stream(context: StoreContext) -> None:
    if context.on_start_build:
        for obj in context.on_start_build:
            loop = GeneratorLoop(
                step=lambda: context.factory.make_one(obj.event_name, date_=date(2023, 1, 1)),
                breaktime_generator=lambda: 1,
                router=context.router,
                pipeline=context.pipeline,
            )
            loop.bootstrap(obj.num_objects)
    
    loops = [
        GeneratorLoop(
            step=lambda: context.event_handler.step(),
            breaktime_generator=lambda: gamma(
                context.breaktime_config.shape,
                context.breaktime_config.scale
            ),
            router=context.router,
            pipeline=context.pipeline,
        ),
    ]

    if context.async_generators:
        loops.extend(
            GeneratorLoop(
                step=lambda: context.factory.make_one(
                    generator.name
                ),
                breaktime_generator=lambda: gamma(
                    generator.breaktime_config.shape,
                    generator.breaktime_config.scale
                ),
                router=context.router,
                pipeline=context.pipeline,
            )
            for generator in context.async_generators
        )

    threads = [Thread(target=loop.run, daemon=True) for loop in loops]

    for t in threads:
        t.start()

    try:
        while any(t.is_alive() for t in threads):
            for t in threads:
                t.join(timeout=0.5)

    except KeyboardInterrupt:
        print("Stopping...")
        for loop in loops:
            loop.stop()
        for t in threads:
            t.join()
        print("Stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RetailFlow store runner")
    parser.add_argument(
        "store",
        choices=BUILDERS.keys(),
        help="Which store to run (alpha or beta)",
    )
    args = parser.parse_args()

    load_handlers()
    builder = BUILDERS[args.store]()

    context = StoreContext.build(builder, args.store)
    run_stream(context)
