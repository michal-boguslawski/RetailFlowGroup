from domain.models import ClickstreamEvent, OrderEvent
from domain.types import GeneratedRecord

from infrastructure.kafka.serializer import AvroSerializerService
from infrastructure.kafka.producer import KafkaProducerClient


class KafkaSink:
    def __init__(
        self,
        kafka_client: KafkaProducerClient,
        serializer: AvroSerializerService
    ):
        self.kafka_client = kafka_client
        self.serializer = serializer

    def write(self, record: GeneratedRecord) -> None:
        match record:
            case ClickstreamEvent():
                serialized = self.serializer("clickstreams", record)
                self.kafka_client.produce("clickstreams", serialized)
            case OrderEvent():
                serialized = self.serializer("orders", record)
                self.kafka_client.produce("orders", serialized)
        print(f"Saved to Kafka: {record}")

    def flush(self) -> None:
        self.kafka_client.flush()

    def close(self) -> None:
        self.kafka_client.flush()
