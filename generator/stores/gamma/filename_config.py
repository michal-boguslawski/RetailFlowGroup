from datetime import date
from typing import Any, Callable

from domain.models import Product, Order, OrderReturn, Promotion


def _get_filename_orders_template(date_: date, *args, **kwargs) -> tuple[str, str]:
    return f"orders_{date_.strftime('%Y%m%d')}", "csv"


def _get_filename_returns_template(date_: date, warehouse_id: str, *args, **kwargs) -> tuple[str, str]:
    return f"returns_WH-{warehouse_id}_{date_.strftime('%Y%m%d')}", "json"


def _get_filename_catalog_template(date_: date, *args, **kwargs) -> tuple[str, str]:
    return f"catalog_{date_.strftime('%Y%m%d')}", "json"


def _get_filename_promotion_template(*args, **kwargs) -> tuple[str, str]:
    return "promotions_weekly", "json"


class FileNamingConfig:
    def __init__(self):
        self._filename_generator: dict[str, Callable[..., tuple[str, str]]] = {
            "orders": _get_filename_orders_template,
            "order_returns": _get_filename_returns_template,
            "products": _get_filename_catalog_template,
            "promotions": _get_filename_promotion_template,
        }

    def get_filename(self, event_type: str, *args, **kwargs) -> tuple[str, str]:
        if event_type not in self._filename_generator:
            raise ValueError(f"Unknown event type: {event_type}")

        return self._filename_generator[event_type](*args, **kwargs)

