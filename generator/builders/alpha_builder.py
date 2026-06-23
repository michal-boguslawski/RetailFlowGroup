from pathlib import Path

from config.models import StoreConfig
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.session.handler_registry import registry
from generator.session.machine import StateMachine
from generator.session.transitions import TransitionMap
from generator.session.profiles.alpha import TRANSITIONS
from generator.schemas.clickstreams.alpha import ClickstreamEvent
from generator.schemas.orders.alpha import OrderEvent
from generator.stores.alpha.router import AlphaRouter
from generator.stores.alpha.factories.clickstream import AlphaClickstreamFactory
from generator.stores.alpha.factories.order import AlphaOrderFactory
from generator.stores.alpha.factories.user import AlphaUserFactory
from generator.stores.alpha.mappers.clickstream import clickstream_renderer
from generator.stores.alpha.mappers.order import order_renderer
from generator.stores.factory import StoreFactory
from infrastructure.kafka.factory import build_kafka_config
from infrastructure.kafka.serializer import AvroSerializerService
from infrastructure.kafka.producer import KafkaProducerClient
from infrastructure.postgres.factory import build_alpha_db_service
from sinks.postgres import PostgresSink
from sinks.kafka import KafkaSink


class AlphaBuilder:
    def build_postgres_sink(self, config: StoreConfig) -> PostgresSink:
        db_service = build_alpha_db_service()
        return PostgresSink(db_service)

    def build_kafka_sink(self, config: StoreConfig) -> KafkaSink:
        kafka_config = build_kafka_config(config.store_id)
        kafka_client = KafkaProducerClient(kafka_config)
        serializer = AvroSerializerService(kafka_config.schema_registry_url, config.store_id)
        serializer.register_serializer("clickstreams", ClickstreamEvent, clickstream_renderer)
        serializer.register_serializer("orders", OrderEvent, order_renderer)
        return KafkaSink(kafka_client, serializer)
    
    def build_router(self, config: StoreConfig) -> AlphaRouter:
        # --- sinks ---
        kafka_sink = self.build_kafka_sink(config)
        postgres_sink = self.build_postgres_sink(config)

        # --- router ---
        return AlphaRouter(kafka_sink, postgres_sink)

    def build_factory(self, config: StoreConfig) -> StoreFactory:
        faker = make_faker(locale="en_US")
        state_path = Path(config.state_path) if config.state_path else None
        ids = IdGenerator(config.store_id, config.ids, state_path=state_path)
        pg_service = build_alpha_db_service()
        alpha_factories = {
            "clickstreams": AlphaClickstreamFactory(ids, pg_service, faker, 100),
            "orders": AlphaOrderFactory(ids, faker, 100),
            "users": AlphaUserFactory(ids, faker),
        }
        return StoreFactory(alpha_factories)

    def build_handler(self, config: StoreConfig) -> StateMachine:
        faker = make_faker(locale="en_US")
        store_factory = self.build_factory(config)
        db_service = build_alpha_db_service()
        transition_map = TransitionMap(TRANSITIONS, fake=faker)
        state_path = Path(config.state_path) if config.state_path else None
        id_generator = IdGenerator(config.store_id, config.ids, state_path)
        handler_registry = registry

        state_machine = StateMachine(
            store_factory,
            db_service,
            transition_map,
            id_generator,
            session=None,
            handler_registry=handler_registry,
        )

        return state_machine
