from argparse import ArgumentParser

from infrastructure.postgres.admin import PostgresAdminClient
from infrastructure.postgres.config import AlphaPostgresConfig, ControlPostgresConfig
from infrastructure.postgres.session import create_engine_from_settings


def reset_postgres(mode: str, store: str):
    config = AlphaPostgresConfig() if store == "alpha" else ControlPostgresConfig()
    engine = create_engine_from_settings(config)
    admin = PostgresAdminClient(engine, store)

    match mode:

        case "truncate":
            admin.truncate_tables()

        case "schema":
            admin.reset_schema()

        case _:
            raise ValueError(mode)


def parse_args():

    parser = ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=[
            "truncate",
            "schema",
        ],
        required=True,
    )

    parser.add_argument(
        "--store",
        choices=[
            "alpha",
            "metadata",
        ],
        required=True,
    )

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    reset_postgres(args.mode, args.store)
