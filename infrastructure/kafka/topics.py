from dataclasses import dataclass
from pathlib import Path

import yaml

from domain.enums import EntityType, StoreId

_DEFAULT_TOPICS_PATH = "infrastructure/config/topics.yaml"


@dataclass
class TopicConfig:
    name: str
    partitions: int
    replication_factor: int
    producer_acks: str = "all"


@dataclass
class InfrastructureTopics:
    minio_notifications: dict[str, TopicConfig]


def _load_yaml(path: str = _DEFAULT_TOPICS_PATH) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_store_topics(store_id: StoreId, path: str = _DEFAULT_TOPICS_PATH) -> dict[EntityType, TopicConfig]:
    raw = _load_yaml(path)
    return {
        EntityType(name.lower()): TopicConfig(**data)
        for name, data in raw[store_id.value].items()
    }


def load_infrastructure_topics(path: str = _DEFAULT_TOPICS_PATH) -> InfrastructureTopics:
    raw = _load_yaml(path)
    return InfrastructureTopics(
        minio_notifications={
            k: TopicConfig(**v) for k, v in raw["infrastructure"]["minio_notifications"].items()
        }
    )
