from datetime import datetime
import json
from pyspark.sql import SparkSession, DataFrame

from infrastructure.kafka.config import KafkaConfig


class MongoConnector:
    def __init__(
        self,
        kafka_config: KafkaConfig | None = None
    ):
        self._kafka_config = kafka_config or KafkaConfig()

    def read_batch(
        self,
        spark: SparkSession,
        database: str,
        collection: str,
        date_since: datetime | None = None,
        date_field: str = "updatedAt",
    ) -> DataFrame:
        reader = (
            spark.read
            .format("mongodb")
            .option("database", database)
            .option("collection", collection)
        )

        if date_since is not None:
            pipeline = [
                {
                    "$addFields": {
                        "_normalized_updated_at": {
                            "$convert": {
                                "input": f"${date_field}",
                                "to": "date",
                                "onError": None,
                                "onNull": None,
                            }
                        }
                    }
                },
                {
                    "$match": {
                        "_normalized_updated_at": {"$gt": {"$date": date_since.isoformat() + "Z"}}
                    }
                },
            ]
            reader = reader.option("aggregation.pipeline", json.dumps(pipeline))

        return reader.load()
