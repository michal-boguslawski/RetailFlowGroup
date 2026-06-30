from pathlib import Path

from config.models import StoreConfig
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.schemas.clickstreams.beta import ClickstreamEvent
from generator.schemas.orders.beta import OrderEvent
from generator.session.handler_registry import registry
from generator.session.machine import StateMachine
from generator.session.transitions import TransitionMap
# from generator.session.profiles.beta import TRANSITIONS
from generator.stores.beta.router import BetaRouter
from generator.stores.beta.mappers.clickstream import clickstream_renderer
from generator.stores.beta.mappers.order import order_renderer
from generator.stores.beta.factories.user import BetaUserFactory
from generator.stores.factory import StoreFactory
from infrastructure.mongo.factory import build_beta_db_service
from infrastructure.kafka.factory import build_kafka_config
from infrastructure.kafka.serializer import AvroSerializerService
from infrastructure.kafka.producer import KafkaProducerClient
from sinks.mongo import MongoSink
from sinks.kafka import KafkaSink


class BetaBuilder:
    def build_mongo_sink(self, config: StoreConfig):
        db_service = build_beta_db_service()
        return MongoSink(db_service)

    def build_kafka_sink(self, config: StoreConfig) -> KafkaSink:
        kafka_config = build_kafka_config(config.store_id)
        kafka_client = KafkaProducerClient(kafka_config)
        serializer = AvroSerializerService(kafka_config.schema_registry_url, config.store_id)
        serializer.register_serializer("clickstreams", ClickstreamEvent, clickstream_renderer)
        serializer.register_serializer("orders", OrderEvent, order_renderer)
        return KafkaSink(kafka_client, serializer)

    def build_router(self, config: StoreConfig) -> BetaRouter:
        # --- sinks ---
        kafka_sink = self.build_kafka_sink(config)
        mongo_sink = self.build_mongo_sink(config)

        # --- router ---
        return BetaRouter(kafka_sink, mongo_sink)

    def build_factory(self, config: StoreConfig) -> StoreFactory:
        faker = make_faker(locale="en_US")
        state_path = Path(config.state_path) if config.state_path else None
        ids = IdGenerator(config.store_id, config.ids, state_path=state_path)
        mongo_service = build_beta_db_service()
        beta_factories = {
            # "clickstreams": AlphaClickstreamFactory(ids, pg_service, faker, 100),
            # "orders": AlphaOrderFactory(ids, faker, 100),
            "users": BetaUserFactory(ids, mongo_service, faker)
        }
        return StoreFactory(beta_factories)

    # def build_handler(self, config: StoreConfig) -> StateMachine:
    #     faker = make_faker(locale="en_US")
    #     store_factory = self.build_factory(config)
    #     db_service = build_beta_db_service()
        # transition_map = TransitionMap(TRANSITIONS, fake=faker)
        # state_path = Path(config.state_path) if config.state_path else None
        # id_generator = IdGenerator(config.store_id, config.ids, state_path)
        # handler_registry = registry

        # state_machine = StateMachine(
        #     store_factory,
        #     db_service,
        #     transition_map,
        #     id_generator,
        #     session=None,
        #     handler_registry=handler_registry,
        # )

        # return state_machine
        