from pathlib import Path
from pydantic import BaseModel, ConfigDict
import yaml


class JobConfig(BaseModel):
    app_name: str
    source: str
    store: str
    entity: str
    target: str
    shuffle_partitions: int = 2
    


class SparkConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    job: JobConfig


def load_spark_config(job: str) -> SparkConfig:
    path = Path("config/jobs") / f"{job}.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    return SparkConfig(**data)


if __name__ == "__main__":
    config = load_spark_config("alpha_orders")
    print(config)
