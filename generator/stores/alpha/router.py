from domain.enums import OrderEventType
from domain.types import GeneratedRecord
from domain.models import User, OrderEvent, ClickstreamEvent
from generator.stores.base import BaseRouter
from sinks.base import BaseSink
from sinks.postgres import PostgresSink


class AlphaRouter(BaseRouter):
    def __init__(self, kafka_sink, postgres_sink: PostgresSink):
        self.kafka_sink = kafka_sink
        self.postgres_sink = postgres_sink

    def route(self, record: GeneratedRecord) -> tuple[BaseSink, ...]:
        match record:
            case OrderEvent(event_type=OrderEventType.PAYMENT_CONFIRMED):
                return (
                    self.kafka_sink,
                    self.postgres_sink,
                )

            case OrderEvent():
                return (
                    self.kafka_sink,
                )

            case ClickstreamEvent():
                return (
                    self.kafka_sink,
                )

            case User():
                return (
                    self.postgres_sink,
                )

            case _:
                raise ValueError(
                    f"No route for {type(record).__name__}"
                )
