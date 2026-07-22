from dataclasses import dataclass


@dataclass(frozen=True)
class JobContract:
    app_name: str
    shuffle_partitions: int
