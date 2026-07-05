from domain.models import GammaOrder, GammaProduct, OrderReturn, Promotion, User
from domain.types import GeneratedRecord
from generator.stores.base import BaseRouter
from sinks.base import BaseSink
from sinks.file import FileSink


class GammaRouter(BaseRouter):
    def __init__(self, file_sink: FileSink):
        self.file_sink = file_sink

    def route(self, record: GeneratedRecord) -> tuple[BaseSink, ...]:
        match record:
            case GammaOrder():
                return (self.file_sink, )

            case GammaProduct():
                return (self.file_sink, )

            case OrderReturn():
                return (self.file_sink, )

            case Promotion():
                return (self.file_sink, )

            case User():
                return tuple()

            case _:
                raise ValueError(
                    f"No route for {type(record).__name__}"
                )
