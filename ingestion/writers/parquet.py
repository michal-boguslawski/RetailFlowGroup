from pyspark.sql import DataFrame
from pyspark.sql.streaming.query import StreamingQuery


class ParquetWriter:
    @staticmethod
    def write_batch(
        df: DataFrame,
        target_path: str,
        partition_cols: list[str] | None = None,
    ) -> None:
        writer = (
            df.write
            .mode("append")
            .format("parquet")
            .option(
                "compression",
                "snappy",
            )
        )

        if partition_cols:
            writer = writer.partitionBy(*partition_cols)

        writer.save(target_path)

    @staticmethod
    def write_stream(
        df: DataFrame,
        target_path: str,
        checkpoint_path: str,
        partition_cols: list[str] | None = None,
    ) -> StreamingQuery:
        writer = (
            df.writeStream
            .format("parquet")
            .option(
                "checkpointLocation",
                checkpoint_path,
            )
            .outputMode("append")
        )

        if partition_cols:
            writer = writer.partitionBy(*partition_cols)
        
        return writer.start(target_path)
        