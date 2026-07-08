import logging
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from infrastructure.kafka.topics import TopicConfig


logger = logging.Logger(__file__)


class KafkaAdminClient:
    def __init__(self, bootstrap_servers: str, topics: dict[str, TopicConfig]):
        self._bootstrap_servers = bootstrap_servers
        self._topics = topics
        self._admin = AdminClient({"bootstrap.servers": bootstrap_servers})

    def ensure_topics(self) -> None:
        existing = self._admin.list_topics().topics
        new_topics = [
            NewTopic(topic.name, num_partitions=topic.partitions, replication_factor=topic.replication_factor)
            for topic in self._topics.values()
            if topic.name not in existing
        ]
        if new_topics:
            self._admin.create_topics(new_topics)
            logger.info(f"Created topics: {[t.topic for t in new_topics]}")
        else:
            logger.info("All topics already exist, skipping creation")

    def delete_topics(self):
        topic_names = [t.name for t in self._topics.values()]
        existing = self._admin.list_topics().topics
        to_delete = [name for name in topic_names if name in existing]

        if not to_delete:
            logger.info("No topics to delete")
            return

        delete_futures = self._admin.delete_topics(to_delete)
        for topic, future in delete_futures.items():
            try:
                future.result()
                logger.info(f"Deleted topic: {topic}")
            except Exception as e:
                logger.warning(f"Could not delete {topic}: {e}")

    def reset_topics(self):
        self.delete_topics()
        self.ensure_topics()
