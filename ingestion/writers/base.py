from typing import Protocol, Callable
from pyspark.sql import DataFrame
from pyspark.sql.streaming.query import StreamingQuery

class Writer(Protocol):
    def write_batch(self, df: DataFrame, path: str, partition_cols: list[str] | None = None) -> None: ...

    def write_stream(
        self,
        df: DataFrame,
        checkpoint_path: str,
        process_batch: Callable[[DataFrame, int], None],
        trigger_interval: str = "1 minute",
        partition_cols: list[str] | None = None,
    ) -> StreamingQuery: ...