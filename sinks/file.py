from dataclasses import dataclass, field
from collections import defaultdict
import csv
import json
from io import StringIO

from domain.enums import Country
from domain.models import GammaOrder, OrderReturn, GammaProduct, Promotion, Formatter
from domain.types import GeneratedRecord
from infrastructure.minio.service import S3Service
from generator.stores.gamma.filename_config import FileNamingConfig
from generator.stores.gamma.mappers.order import model_to_dict as order_to_dict
from generator.stores.gamma.mappers.product import model_to_dict as product_to_dict
from generator.stores.gamma.mappers.promotion import model_to_dict as promotion_to_dict
from generator.stores.gamma.mappers.order_return import model_to_dict as order_return_to_dict
from sinks.base import BaseSink


def records_to_csv_bytes(
    rows: list[dict],
    encoding: str = "utf-8",
    end_row: dict | str | None = None,
) -> bytes:
    if not rows:
        return b""

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

    if end_row is not None:
        if isinstance(end_row, dict):
            writer.writerow(end_row)
        else:
            writer.writer.writerow([end_row])  # plain single-cell row, e.g. "TOTAL: 1234.56"

    return buffer.getvalue().encode(encoding, errors="strict")


def records_to_json_bytes(rows: list[dict], encoding: str = "utf-8") -> bytes:
    return json.dumps(rows, ensure_ascii=False, default=str).encode(encoding, errors="strict")


RECORDS_ENCODERS = {
    "csv": records_to_csv_bytes,
    "json": records_to_json_bytes,
}


@dataclass
class WriteBuffer:
    orders: list[GammaOrder] = field(default_factory=list)
    order_returns: dict[Country, list[OrderReturn]] = field(
        default_factory=lambda: defaultdict(list)
    )
    products: list[GammaProduct] = field(default_factory=list)
    promotions: list[Promotion] = field(default_factory=list)


class FileSink(BaseSink):
    def __init__(self, s3_service: S3Service, naming_config: FileNamingConfig, bucket_name: str):
        self.s3_service = s3_service
        self.naming_config = naming_config
        self.buffer: WriteBuffer = WriteBuffer()
        self.bucket_name = bucket_name


    def write(self, record: GeneratedRecord):
        match record:
            case GammaOrder():
                self.buffer.orders.append(record)
            case OrderReturn():
                self.buffer.order_returns[record.country].append(record)
            case GammaProduct():
                self.buffer.products.append(record)
            case Promotion():
                self.buffer.promotions.append(record)
            case Formatter():
                self.flush(record)
        print(f"Received {type(record).__name__}")

    def bulk_write(self, records: list[GeneratedRecord]):
        for record in records:
            self.write(record)

    def _flush_orders(self, formatter: Formatter):
        orders_dicts = [order_to_dict(o, formatter) for o in self.buffer.orders]
        order_filename, order_extension = self.naming_config.get_filename("orders", date_=formatter.current_date)
        encoder = RECORDS_ENCODERS[order_extension]
        self.s3_service.upload_bytes(
            self.bucket_name,
            f"raw/orders/{order_filename}.{order_extension}",
            encoder(orders_dicts),
            f"text/{order_extension}; charset=windows-1250",
        )
        self.buffer.orders.clear()
        print(f"Flushed {len(orders_dicts)} orders")

    def _flush_products(self, formatter: Formatter):
        products_dicts = [product_to_dict(p, formatter) for p in self.buffer.products]
        product_filename, product_extension = self.naming_config.get_filename("products", date_=formatter.current_date)
        encoder = RECORDS_ENCODERS[product_extension]
        self.s3_service.upload_bytes(
            self.bucket_name,
            f"raw/products/{product_filename}.{product_extension}",
            encoder(products_dicts),
            f"text/{product_extension}; charset=utf-8",
        )
        self.buffer.products.clear()
        print(f"Flushed {len(products_dicts)} products")

    def _flush_promotions(self, formatter: Formatter):
        promotions_dicts = [promotion_to_dict(p, formatter) for p in self.buffer.promotions]
        promotion_filename, promotion_extension = self.naming_config.get_filename("promotions")
        encoder = RECORDS_ENCODERS[promotion_extension]
        end_row = formatter.totals_generator_fn(self.buffer.promotions)
        self.s3_service.upload_bytes(
            self.bucket_name,
            f"raw/promotions/{promotion_filename}.{promotion_extension}",
            encoder(promotions_dicts, encoding="utf-8-sig", end_row=end_row),
            f"text/{promotion_extension}; charset=utf-8",
        )

    def _flush_order_returns(self, formatter: Formatter, warehouse: Country):
        order_returns = self.buffer.order_returns.get(warehouse)
        if order_returns:
            order_returns_dicts = [order_return_to_dict(or_, formatter) for or_ in order_returns]
            order_return_filename, order_return_extension = self.naming_config.get_filename(
                "order_returns", date_=formatter.current_date, warehouse_id=warehouse.value
            )
            encoder = RECORDS_ENCODERS[order_return_extension]
            self.s3_service.upload_bytes(
                self.bucket_name,
                f"raw/returns/{order_return_filename}.{order_return_extension}",
                encoder(order_returns_dicts),
                f"text/{order_return_extension}; charset=utf-8",
            )
            self.buffer.order_returns[warehouse].clear()
            print(f"Flushed {len(order_returns_dicts)} order returns for {warehouse}")

    def flush(self, formatter: Formatter):
        if self.buffer.orders:
            self._flush_orders(formatter)

        if self.buffer.promotions:
            self._flush_promotions(formatter)
        
        if self.buffer.products:
            self._flush_products(formatter)

        for key, value in self.buffer.order_returns.items():
            if value:
                self._flush_order_returns(formatter, key)
        
    def close(self):
        pass
