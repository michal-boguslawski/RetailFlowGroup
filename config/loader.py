from pathlib import Path
import yaml

from config.models import StoreConfig, LakeConfig


def load_config(store_id: str) -> StoreConfig:
    path = Path("config") / f"{store_id}.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    return StoreConfig(**data)


def load_lake_config(path: Path = Path("infrastructure/config/lake.yaml")) -> LakeConfig:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return LakeConfig.model_validate(raw)


if __name__ == "__main__":
    config = load_config("alpha")
    print(config)
