from typing import Any, Protocol

from pyspark.sql import SparkSession
from pyspark.sql.streaming.query import StreamingQuery

from ingestion.jobs.kafka_to_bronze import kafka_avro_bronze_job_builder
from ingestion.contracts.ingestion import IngestionContract
from infrastructure.core.db_service import DBService
from ingestion.writers.base import Writer


class IngestionJob(Protocol):
    def run_batch(self, spark: SparkSession) -> None: ...
    def run_streaming(self, spark: SparkSession) -> StreamingQuery: ...


class IngestionJobBuilder(Protocol):
    def __call__(self, ingestion_contract: IngestionContract, control_db_service: DBService, writer: Writer) -> IngestionJob: ...


JOB_BUILDER_REGISTRY: dict[str, IngestionJobBuilder] = {
    "kafka": kafka_avro_bronze_job_builder
}


def build_job(ingestion_contract: IngestionContract, control_db_service: DBService, writer: Writer):

    return JOB_BUILDER_REGISTRY[ingestion_contract.source.type](
        ingestion_contract=ingestion_contract,
        control_db_service=control_db_service,
        writer=writer,
    )
