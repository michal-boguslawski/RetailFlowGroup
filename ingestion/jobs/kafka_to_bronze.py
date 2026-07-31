from datetime import date, datetime
from dataclasses import dataclass
from typing import Any, Sequence, cast
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.streaming.query import StreamingQuery

from domain.enums import OffsetWriter
from domain.models.metadata import KafkaOffsetRecord
from infrastructure.core.db_service import DBService
from infrastructure.kafka.config import KafkaConfig
from infrastructure.lake import LAKE_PATHS_RESOLVERS
from ingestion.connectors.kafka import KafkaConnector
from ingestion.connectors.avro import AvroConnector
from ingestion.contracts.ingestion import IngestionContract
from ingestion.writers.base import Writer


@dataclass
class KafkaAvroBronzeIngestionJob:
    ingestion_contract: IngestionContract
    kafka_connector: KafkaConnector
    avro_connector: AvroConnector
    writer: Writer
    control_db_service: DBService

    @property
    def _topic(self) -> str:
        return self.ingestion_contract.source.options["topic"]

    def _get_starting_offsets(self) -> Sequence[KafkaOffsetRecord] | None:
        starting_offsets = self.control_db_service.get_all("kafka_offsets", self._topic)
        assert starting_offsets is None or all(
            isinstance(s, KafkaOffsetRecord) for s in starting_offsets
        ), "starting_offset is wrong"
        return cast(Sequence[KafkaOffsetRecord] | None, starting_offsets)

    def extract_batch(self, spark: SparkSession) -> DataFrame:
        return self.kafka_connector.read_batch(
            spark,
            topic=self._topic,
            starting_offsets=self._get_starting_offsets(),
        )

    def extract_streaming(self, spark: SparkSession) -> DataFrame:
        return self.kafka_connector.read_stream(
            spark,
            topic=self._topic,
            starting_offsets=self._get_starting_offsets(),
        )

    def _compute_ending_offsets(self, df: DataFrame, topic: str, writer: OffsetWriter) -> list[KafkaOffsetRecord]:
        rows = (
            df.groupBy("partition")
            .agg({"offset": "max"})
            .collect()
        )
        return [
            KafkaOffsetRecord(
                topic=topic,
                partition=row["partition"],
                offset=row["max(offset)"] + 1,
                writer=writer,
            )
            for row in rows
        ]

    def _write_and_commit(self, raw_df: DataFrame, path: str, writer: OffsetWriter) -> int:
        """Decodes, writes and commits offsets for one micro-batch or batch run.
        Returns number of rows written."""
        decoded_df = self.avro_connector.decode_batch(raw_df)
        self.writer.write_batch(decoded_df, path)
        self.control_db_service.bulk_save(
            "kafka_offsets", self._compute_ending_offsets(raw_df, self._topic, writer)
        )
        return decoded_df.count()

    def _process_micro_batch(self, batch_df: DataFrame, batch_id: int) -> None:
        if batch_df.isEmpty():
            print("Empty batch, skipping")
            return
        path = self._resolve_write_path(datetime.now().date())
        rows_written = self._write_and_commit(batch_df, path, OffsetWriter.STREAMING)
        print(f"[batch {batch_id}] wrote {rows_written} rows to {path}")

    def _resolve_write_path(self, run_date: date) -> str:
        resolver = LAKE_PATHS_RESOLVERS[self.ingestion_contract.target.layer]
        return resolver(
            store=self.ingestion_contract.dataset.store.value,
            entity=self.ingestion_contract.dataset.entity.value,
            dt=run_date,
        )

    def _resolve_checkpoint_path(self) -> str:
        resolver = LAKE_PATHS_RESOLVERS["checkpoint"]
        return resolver(
            store=self.ingestion_contract.dataset.store.value,
            entity=self.ingestion_contract.dataset.entity.value,
        )

    def _delete_path(self, spark: SparkSession, path: str) -> None:
        assert spark._jsc is not None and spark._jvm is not None, "JVM bridge not available"
        jsc: Any = spark._jsc
        jvm: Any = spark._jvm
        hadoop_conf = jsc.hadoopConfiguration()
        HadoopPath = jvm.org.apache.hadoop.fs.Path
        jvm_path = HadoopPath(path)
        fs = jvm_path.getFileSystem(hadoop_conf)
        if fs.exists(jvm_path):
            fs.delete(jvm_path, True)

    def _reset_checkpoint_if_needed(self, checkpoint_path: str):
        offsets = self._get_starting_offsets()
        if offsets is None:
            # reset checkpoint to beginning
            return

        if any(offset.writer == OffsetWriter.STREAMING for offset in offsets):
            # reset checkpoint to beginning
            print(f"Resetting checkpoint at {checkpoint_path}")
            spark = SparkSession.builder.getOrCreate()
            self._delete_path(spark, checkpoint_path)

    def run_batch(self, spark: SparkSession, *args, **kwargs) -> None:
        raw_df = self.extract_batch(spark)
        if raw_df.isEmpty():
            print("No new data, skipping offset commit")
            return
        path = self._resolve_write_path(datetime.now().date())
        self._write_and_commit(raw_df, path, OffsetWriter.BATCH)

    def run_streaming(self, spark: SparkSession, *args, **kwargs) -> StreamingQuery:
        checkpoint_path = self._resolve_checkpoint_path()
        self._reset_checkpoint_if_needed(checkpoint_path)
        df = self.extract_streaming(spark)
        return self.writer.write_stream(
            df, checkpoint_path=checkpoint_path, process_batch=self._process_micro_batch
        )


def kafka_avro_bronze_job_builder(
    ingestion_contract: IngestionContract,
    control_db_service: DBService,
    writer: Writer,
) -> KafkaAvroBronzeIngestionJob:
    kafka_config = KafkaConfig()
    kafka_connector = KafkaConnector(kafka_config)
    avro_connector = AvroConnector(kafka_config.schema_registry_docker)
    return KafkaAvroBronzeIngestionJob(
        ingestion_contract=ingestion_contract,
        kafka_connector=kafka_connector,
        avro_connector=avro_connector,
        writer=writer,
        control_db_service=control_db_service,
    )
