from datetime import datetime
import json
from pyspark.sql import SparkSession, DataFrame

from infrastructure.mongo.config import MongoDBConfig


class MongoConnector:
    def __init__(
        self,
        mongo_config: MongoDBConfig | None = None,
    ):
        self._mongo_config = mongo_config or MongoDBConfig(local=False)

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

            # MongoDB config
            .option("spark.mongodb.read.connection.uri", self._mongo_config.uri)
            .option("spark.mongodb.write.connection.uri", self._mongo_config.uri)

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
