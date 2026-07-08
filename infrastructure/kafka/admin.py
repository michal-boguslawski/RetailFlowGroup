import logging
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from infrastructure.kafka.topics import TopicConfig


logger = logging.getLogger(__file__)


class KafkaAdminClient:
    def __init__(self, bootstrap_servers: str, topics: dict[str, TopicConfig]):
        self._bootstrap_servers = bootstrap_servers
        self._topics = topics
        self._admin = AdminClient({"bootstrap.servers": bootstrap_servers})

    def ensure_topics(self) -> None:
        existing = self._admin.list_topics().topics
        print(existing)
        print(self._topics.values())
        new_topics = [
            NewTopic(topic.name, num_partitions=topic.partitions, replication_factor=topic.replication_factor)
            for topic in self._topics.values()
            if topic.name not in existing
        ]
        if new_topics:
            futures = self._admin.create_topics(new_topics)
            for topic, future in futures.items():
                try:
                    future.result()   # Waits for broker response
                    print(f"Created {topic}")
                except Exception as e:
                    print(f"Failed to create {topic}: {e}")
        else:
            print("All topics already exist, skipping creation")

    def delete_topics(self):
        topic_names = [t.name for t in self._topics.values()]
        existing = self._admin.list_topics().topics
        to_delete = [name for name in topic_names if name in existing]

        if not to_delete:
            print("No topics to delete")
            return

        delete_futures = self._admin.delete_topics(to_delete)
        for topic, future in delete_futures.items():
            try:
                future.result()
                print(f"Deleted topic: {topic}")
            except Exception as e:
                print(f"Could not delete {topic}: {e}")

    def reset_topics(self):
        self.delete_topics()
        self.ensure_topics()
