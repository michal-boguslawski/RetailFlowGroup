from infrastructure.config.settings import KafkaSettings
from infrastructure.config.kafka_config import KafkaConfig
from infrastructure.kafka.topics import load_topics
from domain.enums import StoreId


def build_kafka_config(store_id: StoreId) -> KafkaConfig:
    kafka_settings = KafkaSettings()
    topics = load_topics(store_id)
    return KafkaConfig.from_settings(
        kafka_settings,
        store_id,
        topics
    )
