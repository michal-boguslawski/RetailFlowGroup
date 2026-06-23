from argparse import ArgumentParser

from domain.enums import StoreId
from infrastructure.config.settings import KafkaSettings
from infrastructure.config.kafka_config import KafkaConfig
from infrastructure.kafka.admin import KafkaAdminClient
from infrastructure.kafka.topics import load_topics


def initialize_kafka(store_id: StoreId):
    settings = KafkaSettings()
    topics = load_topics(store_id)
    kafka_config = KafkaConfig.from_settings(settings, store_id, topics)
    
    admin_client = KafkaAdminClient(kafka_config)
    admin_client.reset_topics()


def parse_args():
    parser = ArgumentParser(
        description="Reset Kafka topics for a store."
    )

    parser.add_argument(
        "--store-id",
        required=True,
        choices=[store.value for store in StoreId],
        help="Store identifier",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    initialize_kafka(StoreId(args.store_id))
