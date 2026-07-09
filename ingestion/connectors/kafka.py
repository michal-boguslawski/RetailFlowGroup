from pyspark.sql import SparkSession, DataFrame

from infrastructure.config.settings import KafkaSettings


class KafkaConnector:
    def __init__(
        self,
        kafka_config: KafkaSettings | None = None,
    ):
        self._kafka_config = kafka_config or KafkaSettings()

    def read_batch(self, spark: SparkSession, topic: str) -> DataFrame:
        df = (
            spark.read
            .format("kafka")
            .option(
                "kafka.bootstrap.servers",
                self._kafka_config.bootstrap_servers_docker
            )
            .option("subscribe", topic)
            .load()
        )
        return df

    def read_stream(self, spark: SparkSession, topic: str) -> DataFrame:
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
        