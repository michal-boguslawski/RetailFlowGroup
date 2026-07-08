import argparse
from datetime import date
from numpy.random import gamma
from threading import Thread

from generator.builders.registry import BUILDERS
from generator.context import StoreContext
from generator.core.loop import GeneratorLoop
from generator.session.handlers.loader import load_handlers


def run_stream(context: StoreContext, event_type: str, num: int) -> None:
    if context.on_start_build:
        for obj in context.on_start_build:
            loop = GeneratorLoop(
                step=lambda: context.factory.make_one(obj.event_name, date_=date(2023, 1, 1)),
                breaktime_generator=lambda: 1,
                router=context.router,
                pipeline=context.pipeline,
            )
            loop.bootstrap(obj.num_objects)
    
    loop = GeneratorLoop(
        step=lambda: context.event_handler.step(event_type=event_type),
        breaktime_generator=lambda: gamma(
            context.breaktime_config.shape,
            context.breaktime_config.scale
        ),
        router=context.router,
        pipeline=context.pipeline,
        flush=lambda: context.event_handler.flush()
    )
    loop.bootstrap(num)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RetailFlow store runner")
    parser.add_argument(
        "store",
        choices=BUILDERS.keys(),
        help="Which store to run (alpha or beta)",
    )
    parser.add_argument(
        "--event_type",
        default=None,
        help="Which event to generate",
    )
    parser.add_argument(
        "--num",
        help="How many events to generate",
    )
    args = parser.parse_args()

    load_handlers()
    builder = BUILDERS[args.store]()

    context = StoreContext.build(builder, args.store)
    run_stream(context, args.event_type, int(args.num))
