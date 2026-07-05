from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable

from domain.models.order import GammaOrder
from domain.models.promotion import Promotion


@dataclass
class ColumnNamingVariant:
    order_id: str
    user_id: str
    order_date: str
    total_amount: str
    status: str
    product_ids: str
    discount_code: str
    city: str
    promo_code: str
    discount_value: str
    valid_from: str
    valid_to: str
    min_order_value: str
    discount_type: str


@dataclass
class Formatter:
    order_date_formattter_fn: Callable[[date], str]
    amount_formatter_fn: Callable[[GammaOrder], str]
    discount_value_formatter_fn: Callable[[Decimal], Decimal]
    valid_formatter_fn: Callable[[date], str]
    min_order_value_formatter_fn: Callable[[Promotion], str]
    totals_generator_fn: Callable[[list[Promotion]], str]
    column_naming_variants: ColumnNamingVariant
