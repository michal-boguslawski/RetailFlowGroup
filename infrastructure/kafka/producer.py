from confluent_kafka import Producer
from logging import Logger

from infrastructure.config.kafka_config import KafkaConfig


logger = Logger(__file__)


class KafkaProducerClient:
    def __init__(self, kafka_config: KafkaConfig):
        self.kafka_config = kafka_config
        self.store_id = kafka_config.store_id
        self.producer = Producer(
            {
                'bootstrap.servers': kafka_config.bootstrap_servers,
            }
        )
        self._counter = 0
        self.poll_per_steps = 1
        self.producer.poll(0.0)

    def produce(self, topic: str, value: bytes | None) -> None:
        kafka_topic = f"{self.store_id.value}.{topic}"
        self.producer.produce(kafka_topic, value=value, callback=self._delivery_callback)

        self._counter += 1
        if self._counter % self.poll_per_steps == 0:
            self.producer.poll(0.0)

    def _delivery_callback(self, err, msg):
        if err is not None:
            logger.error(f"Delivery failed for {msg.topic()}: {err}")
        else:
            logger.debug(f"Delivered to {msg.topic()} [{msg.partition()}]")

    def flush(self):
        self.producer.flush()
