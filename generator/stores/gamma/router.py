from domain.models import GammaOrder, GammaProduct, OrderReturn, Promotion, User, Formatter
from domain.types import GeneratedRecord
from generator.stores.base import BaseRouter
from sinks.base import BaseSink
from sinks.file import FileSink
from sinks.postgres import PostgresSink


class GammaRouter(BaseRouter):
    def __init__(self, file_sink: FileSink, db_sink: PostgresSink):
        self.file_sink = file_sink
        self.db_sink = db_sink

    def route(self, record: GeneratedRecord) -> tuple[BaseSink, ...]:
        match record:
            case GammaOrder():
                return (self.file_sink, self.db_sink)

            case GammaProduct():
                return (self.file_sink, )

            case OrderReturn():
                return (self.file_sink, self.db_sink)

            case Promotion():
                return (self.file_sink, self.db_sink)

            case User():
                return (self.db_sink, )

            case Formatter():
                return (self.file_sink, )

            case _:
                raise ValueError(
                    f"No route for {type(record).__name__}"
                )
