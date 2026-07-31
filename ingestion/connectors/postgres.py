from datetime import datetime
from pyspark.sql import SparkSession, DataFrame

from infrastructure.postgres.config import BasePostgresConfig, AlphaPostgresConfig


class PostgresConnector:
    def __init__(
        self,
        postgres_config: BasePostgresConfig | None = None,
    ):
        self._postgres_config = postgres_config or AlphaPostgresConfig(local=False)

    def read_batch(
        self,
        spark: SparkSession,
        table: str,
        date_since: datetime | None = None,
        date_field: str = "updated_at",
    ) -> DataFrame:
        reader = (
            spark.read
            .format("jdbc")
            .option("driver", "org.postgresql.Driver")
            .option("url", self._postgres_config.jdbc_url)
            .option("user", self._postgres_config.user)
            .option("password", self._postgres_config.password)
            .option("dbtable", table)
            .option("connectTimeout", "10")
        )

        if date_since is not None:
            reader = reader.option(
                "query", f"SELECT * FROM {table} WHERE {date_field} > '{date_since}'"
            )

        return reader.load()
