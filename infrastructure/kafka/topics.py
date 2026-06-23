from dataclasses import dataclass
import yaml

from domain.enums import EntityType, StoreId


@dataclass
class TopicConfig:
    name: str
    partitions: int
    replication_factor: int
    producer_acks: str = "all"


def load_topics(store_id: StoreId, path: str = "infrastructure/config/topics.yaml") -> dict[EntityType, TopicConfig]:
    with open(path) as f:
        raw = yaml.safe_load(f)

    return {
        EntityType(name.lower()): TopicConfig(**data)
        for name, data in raw[store_id.value].items()
    }
