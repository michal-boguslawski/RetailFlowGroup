from pyspark.sql import SparkSession, DataFrame
from typing import Sequence

from domain.models.metadata import KafkaOffsetRecord
from infrastructure.kafka.config import KafkaConfig
from ingestion.utils import parse_offsets


class KafkaConnector:
    def __init__(
        self,
        kafka_config: KafkaConfig | None = None,
    ):
        self._kafka_config = kafka_config or KafkaConfig()

    def read_batch(self,
                   spark: SparkSession,
                   topic: str,
                   starting_offsets: str | Sequence[KafkaOffsetRecord] | None = None,
                   ending_offsets: str | Sequence[KafkaOffsetRecord] | None = None) -> DataFrame:
        _starting_offsets = parse_offsets(starting_offsets or "earliest", topic)
        _ending_offsets = parse_offsets(ending_offsets or "latest", topic)

        df = (
            spark.read
            .format("kafka")
            .option(
                "kafka.bootstrap.servers",
                self._kafka_config.bootstrap_servers_docker
            )
            .option("subscribe", topic)
            .option("startingOffsets", _starting_offsets)
            .option("endingOffsets", _ending_offsets)
            .load()
        )
        return df

    def read_stream(self,
                    spark: SparkSession,
                    topic: str,
                    starting_offsets: str | Sequence[KafkaOffsetRecord] | None = None,
                    ) -> DataFrame:
        _starting_offsets = parse_offsets(starting_offsets or "earliest", topic)
        df = (
            spark.readStream
            .format("kafka")
            .option(
                "kafka.bootstrap.servers",
                self._kafka_config.bootstrap_servers_docker
            )
            .option("subscribe", topic)
            .option("startingOffsets", _starting_offsets)
            .load()
        )
        return df
        