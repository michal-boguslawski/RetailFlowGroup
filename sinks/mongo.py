from sinks.base import BaseSink
from infrastructure.core.db_service import DBService
from domain.types import GeneratedRecord
from domain.models import BetaUser
from generator.stores.beta.mappers.user import model_to_document as user_model_to_document


class MongoSink(BaseSink):
    def __init__(self, service: DBService):
        self.service = service

    def write(self, record: GeneratedRecord) -> None:
        match record:
            case BetaUser():
                self.service.save("users", user_model_to_document(record))

        print(f"Saved to MongoDB: {record} of type {type(record).__name__}")

    def bulk_write(self, records: list[GeneratedRecord]) -> None:
        if not records:
            return

        match records[0]:
            case BetaUser():
                self.service.bulk_save(
                    "users",
                    [user_model_to_document(r) for r in records if isinstance(r, BetaUser)]
                )

    def flush(self) -> None:
        pass

    def close(self) -> None:
        pass
