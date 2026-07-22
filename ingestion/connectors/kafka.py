from pyspark.sql import SparkSession, DataFrame

from infrastructure.kafka.config import KafkaConfig


class KafkaConnector:
    def __init__(
        self,
        kafka_config: KafkaConfig | None = None,
    ):
        self._kafka_config = kafka_config or KafkaConfig()

    def read_batch(self,
                   spark: SparkSession,
                   topic: str,
                   starting_offsets: str = "earliest",
                   ending_offsets: str = "latest") -> DataFrame:
        df = (
            spark.read
            .format("kafka")
            .option(
                "kafka.bootstrap.servers",
                self._kafka_config.bootstrap_servers_docker
            )
            .option("subscribe", topic)
            .option("startingOffsets", starting_offsets)
            .option("endingOffsets", ending_offsets)
            .load()
        )
        return df

    def read_stream(self,
                    spark: SparkSession,
                    topic: str) -> DataFrame:
        df = (
            spark.readStream
            .format("kafka")
            .option(
                "kafka.bootstrap.servers",
                self._kafka_config.bootstrap_servers_docker
            )
            .option("subscribe", topic)
            .load()
        )
        return df
        