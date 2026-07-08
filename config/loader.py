from pathlib import Path
import yaml

from config.models import StoreConfig


def load_config(store_id: str) -> StoreConfig:
    path = Path("config") / f"{store_id}.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    return StoreConfig(**data)


if __name__ == "__main__":
    config = load_config("alpha")
    print(config)
