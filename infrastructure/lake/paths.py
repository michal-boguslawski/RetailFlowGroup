from datetime import date

from infrastructure.lake.config import lake_config


def bronze_path(*, store: str, entity: str, dt: date) -> str:
    layer = lake_config.bronze

    return (
        f"s3a://{layer.bucket}/"
        + layer.resolve(
            store=store,
            entity=entity,
            date=dt.isoformat(),
        )
    )


def silver_path(*, entity: str, dt: date) -> str:
    layer = lake_config.silver

    return (
        f"s3a://{layer.bucket}/"
        + layer.resolve(
            store="",
            entity=entity,
            date=dt.isoformat(),
        )
    )
