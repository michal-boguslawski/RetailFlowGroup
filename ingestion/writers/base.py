from typing import Protocol, Callable
from pyspark.sql import DataFrame

class Writer(Protocol):
    def write(self, df: DataFrame, path: str, partition_cols: list[str] | None = None) -> None: ...

    def write_stream(
        self,
        df: DataFrame,
        path: str,
        checkpoint_path: str,
        process_batch: Callable[[DataFrame, int], None],
        trigger_interval: str = "1 minute",
        partition_cols: list[str] | None = None,
    ) -> None: ...