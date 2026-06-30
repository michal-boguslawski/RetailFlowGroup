from domain.types import GeneratedRecord
from domain.models import User
from generator.stores.base import BaseRouter
from sinks.base import BaseSink
from sinks.kafka import KafkaSink
from sinks.mongo import MongoSink


class BetaRouter(BaseRouter):
    def __init__(self, kafka_sink: KafkaSink, mongo_sink: MongoSink):
        self.kafka_sink = kafka_sink
        self.mongo_sink = mongo_sink

    def route(self, record: GeneratedRecord) -> tuple[BaseSink, ...]:
        match record:
            case User():
                return (self.mongo_sink, )

            case _:
                raise ValueError(
                    f"No route for {type(record).__name__}"
                )
