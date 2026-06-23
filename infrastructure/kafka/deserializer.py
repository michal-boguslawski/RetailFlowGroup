# infrastructure/kafka/deserializer.py  (or tests/fixtures/ if purely test-scoped — see below)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

from domain.enums import StoreId


class AvroDeserializerService:
    def __init__(self, schema_registry_url: str, store_id: StoreId):
        self.store_id = store_id
        self.schema_registry_client = SchemaRegistryClient({"url": schema_registry_url})
        self._deserializers: dict[str, AvroDeserializer] = {}

    def _build_deserializer(self, topic: str) -> AvroDeserializer:
        # AvroDeserializer can fetch the writer schema from the registry automatically
        # if you don't pass schema_str — only needed if you want strict reader-schema validation
        return AvroDeserializer(
            schema_registry_client=self.schema_registry_client,
            from_dict=lambda data, ctx: data,  # or a reverse-renderer back to your domain dataclass
        )

    def _get_deserializer(self, topic: str) -> AvroDeserializer:
        if topic not in self._deserializers:
            self._deserializers[topic] = self._build_deserializer(topic)
        return self._deserializers[topic]

    def deserialize(self, topic: str, raw: bytes) -> dict | object | None:
        deserializer = self._get_deserializer(topic)
        return deserializer(raw, SerializationContext(topic, MessageField.VALUE))
