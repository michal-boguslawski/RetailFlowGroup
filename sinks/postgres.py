# sinks/postgres_sink.py
from sinks.base import BaseSink
from infrastructure.core.db_service import DBService
from domain.types import GeneratedRecord
from domain.models import User, OrderEvent, Product, OrderReturn, GammaOrder, Promotion


class PostgresSink(BaseSink):
    def __init__(self, service: DBService):
        self.service = service

    def write(self, record: GeneratedRecord) -> None:
        match record:
            case User():
                self.service.save("users", record)
            case OrderEvent():
                self.service.save("orders", record.order)
            case Product():
                self.service.save("products", record)
            case OrderReturn():
                self.service.save("order_returns", record)
            case GammaOrder():
                self.service.save("orders", record)
            case Promotion():
                self.service.save("promotions", record)

        print(f"Saved to Postgres: {record} of type {type(record).__name__}")

    def bulk_write(self, records: list[GeneratedRecord]) -> None:
        if not records:
            return

        match records[0]:
            case User():
                self.service.bulk_save("users", records)
            case OrderEvent():
                self.service.bulk_save(
                    "orders",
                    [r.order for r in records if isinstance(r, OrderEvent)]
                )
            case Product():
                self.service.bulk_save("products", records)
            case OrderReturn():
                self.service.bulk_save("order_returns", records)
            case GammaOrder():
                self.service.bulk_save("orders", records)
            case Promotion():
                self.service.bulk_save("promotions", records)

        print(f"Saved {len(records)} records to Postgres")

    def flush(self) -> None:
        pass

    def close(self) -> None:
        pass
