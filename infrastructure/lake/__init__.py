from typing import Callable

from infrastructure.lake.paths import (
    bronze_path, silver_path, checkpoint_path
)


LAKE_PATHS_RESOLVERS: dict[str, Callable[..., str]] = {
    "bronze": bronze_path,
    "silver": silver_path,
    "checkpoint": checkpoint_path,
}
