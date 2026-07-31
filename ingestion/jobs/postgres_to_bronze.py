from datetime import date, datetime
from dataclasses import dataclass
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.streaming.query import StreamingQuery

from infrastructure.core.db_service import DBService
from infrastructure.postgres.config import AlphaPostgresConfig
from infrastructure.lake import LAKE_PATHS_RESOLVERS
from ingestion.connectors.postgres import PostgresConnector
from ingestion.contracts.ingestion import IngestionContract
from ingestion.writers.base import Writer


@dataclass
class PostgresBronzeIngestionJob:
    ingestion_contract: IngestionContract
    postgres_connector: PostgresConnector
    writer: Writer
    control_db_service: DBService

    def extract_batch(self, spark: SparkSession, date_since: datetime | None = None) -> DataFrame:
        return self.postgres_connector.read_batch(
            spark,
            table=self.ingestion_contract.source.options["table"],
            date_since=date_since,
            date_field=str(self.ingestion_contract.source.options.get("date_field", None))
        )

    def _resolve_write_path(self, run_date: date) -> str:
        resolver = LAKE_PATHS_RESOLVERS[self.ingestion_contract.target.layer]
        return resolver(
            store=self.ingestion_contract.dataset.store.value,
            entity=self.ingestion_contract.dataset.entity.value,
            source=self.ingestion_contract.source.type,
            dt=run_date,
        )

    def _write_and_commit(self, raw_df: DataFrame, path: str) -> int:
        self.writer.write_batch(raw_df, path)
        return raw_df.count()

    def run_batch(self, spark: SparkSession, date_since: datetime | None = None) -> None:
        raw_df = self.extract_batch(spark, date_since=date_since)
        if raw_df.isEmpty():
            print("No new data, skipping offset commit")
            return
        path = self._resolve_write_path(datetime.now().date())
        cnt = self._write_and_commit(raw_df, path)
        print(f"wrote {cnt} rows to {path}")

    def run_streaming(self, spark: SparkSession) -> StreamingQuery:
        raise NotImplementedError("Streaming not implemented for Postgres")


def postgres_bronze_job_builder(
    ingestion_contract: IngestionContract,
    control_db_service: DBService,
    writer: Writer,
) -> PostgresBronzeIngestionJob:
    postgres_config = AlphaPostgresConfig(local=False)
    postgres_connector = PostgresConnector(postgres_config)
    return PostgresBronzeIngestionJob(
        ingestion_contract=ingestion_contract,
        postgres_connector=postgres_connector,
        writer=writer,
        control_db_service=control_db_service,
    )
