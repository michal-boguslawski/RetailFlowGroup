from dataclasses import dataclass
from infrastructure.config.settings import KafkaSettings
from infrastructure.kafka.topics import TopicConfig
from domain.enums import EntityType, StoreId


@dataclass
class KafkaConfig:
    bootstrap_servers: str
    schema_registry_url: str
    store_id: StoreId
    topics: dict[EntityType, TopicConfig]   # only this store's topics, already filtered

    @classmethod
    def from_settings(cls, settings: KafkaSettings, store_id: StoreId, topics: dict[EntityType, TopicConfig]):
        return cls(
            bootstrap_servers=settings.bootstrap_servers,
            schema_registry_url=settings.schema_registry_url,
            store_id=store_id,
            topics=topics,
        )
