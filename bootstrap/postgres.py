from argparse import ArgumentParser

from infrastructure.postgres.admin import PostgresAdminClient
from infrastructure.postgres.config import AlphaPostgresConfig
from infrastructure.postgres.session import create_engine_from_settings


def reset_postgres(mode: str):
    config = AlphaPostgresConfig()
    engine = create_engine_from_settings(config)
    admin = PostgresAdminClient(engine)

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

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    reset_postgres(args.mode)
