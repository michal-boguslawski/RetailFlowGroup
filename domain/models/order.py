from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from domain.enums import (
    StoreId, OrderEventType, Currency
)
from domain.models.product import Product
from domain.models.user import User


@dataclass
class OrderLineItem:
    product: Product
    id: int | None = None
    quantity: Optional[int] = None
    discount_pct: Optional[float] = None

    @property
    def total_amount(self) -> Decimal:
        # print(self.product, type(self.product.price))
        discount_multiplier = (1 - self.discount_pct / 100) if self.discount_pct else 1
        return self.product.price * (self.quantity or 1) * Decimal(discount_multiplier)


@dataclass
class Order:
    id: str
    user: Optional[User]
    guest_email: Optional[str]
    items: list[OrderLineItem]
    currency: Currency
    notes: Optional[str]

    @property
    def total_amount(self) -> Decimal:
        return sum((item.total_amount for item in self.items), Decimal(0))

    @property
    def tax_amount(self) -> Optional[Decimal]:
        if self.total_amount:
            return self.total_amount * Decimal(0.23)  # Assuming 23% tax rate


@dataclass
class OrderEvent:
    event_id: str
    event_type: OrderEventType
    event_ts: int
    store_id: StoreId
    order: Order
    failure_reason: Optional[str]
    schema_version: str
