import argparse
from numpy.random import gamma
from threading import Thread

from generator.builders.registry import BUILDERS
from generator.context import StoreContext
from generator.core.loop import GeneratorLoop
from generator.session.handlers.loader import load_handlers


def run_stream(context: StoreContext) -> None:
    loops = [
        GeneratorLoop(
            step=lambda: context.factory.make_one("users"),
            breaktime_generator=lambda: gamma(10, 2),
            router=context.router,
            pipeline=context.pipeline,
        ),
        GeneratorLoop(
            step=lambda: context.event_handler.step(),
            breaktime_generator=lambda: gamma(0.5, 0.5),
            router=context.router,
            pipeline=context.pipeline,
        ),
    ]

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
