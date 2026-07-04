from argparse import ArgumentParser
from generator.builders.registry import BUILDERS
from generator.core.loop import GeneratorLoop
from generator.context import StoreContext


def parse_args():
    parser = ArgumentParser(description="Bootstrap synthetic users")

    parser.add_argument(
        "store",
        choices=BUILDERS.keys(),
        help="Which store to bootstrap",
    )
    parser.add_argument(
        "--users",
        type=int,
        default=10,
        help="Number of users to generate",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    context = StoreContext.build(BUILDERS[args.store](), args.store)

    loop = GeneratorLoop(
        step=lambda: context.factory.make_one("users"),
        breaktime_generator=lambda: 1,
        router=context.router,
        pipeline=context.pipeline,
    )
    loop.bootstrap(args.users)
