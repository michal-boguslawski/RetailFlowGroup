from datetime import date, datetime
from dataclasses import dataclass
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.streaming.query import StreamingQuery
import time

from infrastructure.lake import LAKE_PATHS_RESOLVERS
from infrastructure.kafka.config import KafkaConfig
from infrastructure.kafka.topics import load_store_topics
from infrastructure.spark.session import create_spark_session
from ingestion.connectors.kafka import KafkaConnector
from ingestion.connectors.avro import AvroConnector
from ingestion.contracts.loader import load_contract
from ingestion.contracts.ingestion import IngestionContract
from ingestion.writers.lake import LakeWriter


@dataclass
class BronzeIngestionJob:
    ingestion_contract: IngestionContract
    kafka_connector: KafkaConnector
    avro_connector: AvroConnector
    writer: LakeWriter

    def extract_batch(self, spark: SparkSession) -> DataFrame:
        return self.kafka_connector.read_batch(
            spark,
            topic=self.ingestion_contract.source.options["topic"]
        )

    def extract_streaming(self, spark: SparkSession) -> DataFrame:
        return self.kafka_connector.read_stream(
            spark,
            topic=self.ingestion_contract.source.options["topic"]
        )

    def transform(self, df: DataFrame) -> DataFrame:
        return self.avro_connector.decode_batch(df)

    def write(self, df: DataFrame, path: str) -> None:
        self.writer.write_batch(df, path)

    def _process_micro_batch(self, batch_df: DataFrame, batch_id: int) -> None:
        if batch_df.isEmpty():
            return
        decoded = self.transform(batch_df)
        run_date = datetime.now().date()
        path = self._resolve_write_path(run_date)
        self.write(decoded, path)
        print(f"[batch {batch_id}] wrote {decoded.count()} rows to {path}")

    def write_streaming(self, df: DataFrame, path: str, checkpoint_path: str) -> StreamingQuery:
        return self.writer.write_stream(
            df,
            path,
            checkpoint_path,
            process_batch=self._process_micro_batch,
        )

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

    def run(self, spark: SparkSession) -> None:
        run_date = datetime.now().date()
        path = self._resolve_write_path(run_date)
        print(path)
        df = self.extract_batch(spark)
        df = self.transform(df)
        self.write(df, path)

    def run_streaming(self, spark: SparkSession) -> StreamingQuery:
        run_date = datetime.now().date()
        path = self._resolve_write_path(run_date)
        checkpoint_path = self._resolve_checkpoint_path()
        df = self.extract_streaming(spark)
        return self.write_streaming(df, path, checkpoint_path)


if __name__ == "__main__":
    ingestion_contract = load_contract("alpha_orders")
    spark = create_spark_session(
        ingestion_contract.job.app_name,
        shuffle_partitions=ingestion_contract.job.shuffle_partitions,
    )

    kafka_connector = KafkaConnector()

    kafka_config = KafkaConfig()
    print(kafka_config.schema_registry_docker)
    avro_connector = AvroConnector(kafka_config.schema_registry_docker)
    writer = LakeWriter()

    job = BronzeIngestionJob(
        ingestion_contract=ingestion_contract,
        kafka_connector=kafka_connector,
        avro_connector=avro_connector,
        writer=writer,
    )
    # try:
    #     job.run(spark)
    # finally:
    #     spark.stop()

    query = job.run_streaming(spark)
    print(query.lastProgress)
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        query.stop()
    finally:
        spark.stop()
