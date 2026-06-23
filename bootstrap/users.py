from argparse import ArgumentParser

from config.loader import load_config
from generator.core.loop import GeneratorLoop
from generator.builders.alpha_builder import AlphaBuilder


def parse_args():
    parser = ArgumentParser(
        description="Generate synthetic users"
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

    config = load_config("alpha")

    alpha_builder = AlphaBuilder()

    alpha_factory = alpha_builder.build_factory(config)
    alpha_router = alpha_builder.build_router(config)

    user_loop = GeneratorLoop(
        step=lambda: alpha_factory.make_one("users"),
        breaktime_generator=lambda: 1,
        router=alpha_router,
        pipeline=None,
    )

    user_loop.bootstrap(args.users)
