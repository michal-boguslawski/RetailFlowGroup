from dataclasses import dataclass
from pyspark.sql import DataFrame
from pyspark.sql.streaming.query import StreamingQuery
from typing import Callable


@dataclass
class LakeWriter:
    format: str = "parquet"
    mode: str = "append"

    def write_batch(
        self,
        df: DataFrame,
        path: str,
        partition_cols: list[str] | None = None,
    ) -> None:
        writer = (
            df.write
            .format(self.format)
            .mode(self.mode)
            .option("compression", "snappy")
        )

        if partition_cols:
            writer = writer.partitionBy(*partition_cols)

        writer.save(path)

    def write_stream(
        self,
        df: DataFrame,
        checkpoint_path: str,
        process_batch: Callable[[DataFrame, int], None],
        trigger_interval: str = "1 minute",
        partition_cols: list[str] | None = None,
        *args,
        **kwargs
    ) -> StreamingQuery:
        writer = (
            df.writeStream
            .foreachBatch(process_batch)
            .option("checkpointLocation", checkpoint_path)
            .trigger(processingTime=trigger_interval)
        )

        if partition_cols:
            writer = writer.partitionBy(*partition_cols)
        
        return writer.start()
