from argparse import ArgumentParser

from domain.enums import StoreId
from infrastructure.kafka.config import KafkaConfig
from infrastructure.kafka.admin import KafkaAdminClient
from infrastructure.kafka.topics import load_store_topics, load_infrastructure_topics


def initialize_store_topics(store_id: StoreId):
    settings = KafkaConfig()
    topics = load_store_topics(store_id)

    admin_client = KafkaAdminClient(
        bootstrap_servers=settings.bootstrap_servers,
        topics={k.value: v for k, v in topics.items()},
    )
    admin_client.reset_topics()


def initialize_infrastructure_topics() -> None:
    settings = KafkaConfig()
    infra_topics = load_infrastructure_topics()  # InfrastructureTopics
    admin_client = KafkaAdminClient(
        settings.bootstrap_servers, infra_topics.minio_notifications
    )
    admin_client.reset_topics()


def parse_args():
    parser = ArgumentParser(description="Reset Kafka topics.")
    subparsers = parser.add_subparsers(dest="target", required=True)

    store_parser = subparsers.add_parser("store", help="Reset topics for a store")
    store_parser.add_argument(
        "--store-id",
        required=True,
        choices=[s.value for s in StoreId],
    )

    subparsers.add_parser("infrastructure", help="Reset infrastructure topics")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.target == "store":
        initialize_store_topics(StoreId(args.store_id))
    else:
        initialize_infrastructure_topics()
