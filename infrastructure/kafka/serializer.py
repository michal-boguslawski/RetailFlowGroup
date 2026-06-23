from typing import Optional
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

from domain.enums import StoreId
from domain.models import ClickstreamEvent, OrderEvent
from schemas.factory import build_avro_schema
from infrastructure.kafka.renderers.factory import build_renderer


class AvroSerializerService:
    def __init__(self, schema_registry_url: str, store_id: StoreId):
        self.store_id = store_id
        self.schema_registry_client = SchemaRegistryClient(
            {"url": schema_registry_url}
        )
        self._serializers: dict[str, AvroSerializer] = {}

    def _build_serializer(self, topic: str):
        schema_str = build_avro_schema(topic, self.store_id.value)
        renderer = build_renderer(topic, self.store_id.value)

        self._serializers[topic] = AvroSerializer(
            schema_registry_client=self.schema_registry_client,
            schema_str=schema_str,
            to_dict=renderer,
        )

    def _get_serializer(self, topic: str) -> AvroSerializer:
        if topic not in self._serializers:
            self._build_serializer(topic)

        return self._serializers[topic]

    def __call__(self, topic: str, value: OrderEvent | ClickstreamEvent) -> bytes | None:
        serializer = self._get_serializer(topic)
        
        return serializer(
            value,
            SerializationContext(topic, MessageField.VALUE)
        )
