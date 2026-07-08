from pathlib import Path
import yaml

from infrastructure.lake.models import LakeConfig


def load_lake_config(path: Path = Path("infrastructure/config/lake.yaml")) -> LakeConfig:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return LakeConfig.model_validate(raw)


lake_config = load_lake_config()
