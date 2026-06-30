from argparse import ArgumentParser

from config.loader import load_config
from generator.core.loop import GeneratorLoop
from generator.builders.alpha_builder import AlphaBuilder
from generator.builders.beta_builder import BetaBuilder
from generator.pipeline.builder import build_pipeline


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


def generate_alpha_loop() -> GeneratorLoop:
    config = load_config("alpha")

    alpha_builder = AlphaBuilder()

    alpha_factory = alpha_builder.build_factory(config)
    alpha_router = alpha_builder.build_router(config)

    pipeline = build_pipeline(config.pipeline_config) if config.pipeline_config else None

    user_loop = GeneratorLoop(
        step=lambda: alpha_factory.make_one("users"),
        breaktime_generator=lambda: 1,
        router=alpha_router,
        pipeline=pipeline,
    )
    return user_loop


def generate_beta_loop() -> GeneratorLoop:
    config = load_config("beta")

    beta_builder = BetaBuilder()

    beta_factory = beta_builder.build_factory(config)
    beta_router = beta_builder.build_router(config)

    pipeline = build_pipeline(config.pipeline_config) if config.pipeline_config else None

    user_loop = GeneratorLoop(
        step=lambda: beta_factory.make_one("users"),
        breaktime_generator=lambda: 1,
        router=beta_router,
        pipeline=pipeline,
    )
    return user_loop
    


if __name__ == "__main__":
    args = parse_args()

    # user_loop = generate_alpha_loop()
    user_loop = generate_beta_loop()

    user_loop.bootstrap(args.users)
