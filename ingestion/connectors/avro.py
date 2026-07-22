import struct

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import udf, col, substring, length
from pyspark.sql.types import IntegerType
from pyspark.sql.avro.functions import from_avro
from confluent_kafka.schema_registry import SchemaRegistryClient

class AvroConnector:
    def __init__(self, schema_registry_url: str):
        self._client = SchemaRegistryClient({"url": schema_registry_url})

    @staticmethod
    @udf(IntegerType())
    def extract_schema_id(raw: bytes) -> int:
        return struct.unpack(">I", raw[1:5])[0]

    def decode(self, df: DataFrame):
        df_with_id = df.withColumn("schema_id", self.extract_schema_id(col("value")))
        present_ids = [r.schema_id for r in df_with_id.select("schema_id").distinct().collect()]

        decoded_parts = []
        for schema_id in present_ids:
            schema_str = self._client.get_schema(schema_id).schema_str
            if schema_str is None:
                raise ValueError(f"Schema with id {schema_id} not found")

            part = (
                df_with_id
                .filter(col("schema_id") == schema_id)
                .withColumn(
                    "parsed",
                    from_avro(substring(col("value"), 6, length(col("value")) - 5), schema_str),
                )
            )
            decoded_parts.append(part)

        result = decoded_parts[0]
        for part in decoded_parts[1:]:
            result = result.unionByName(part, allowMissingColumns=True)
        return result
