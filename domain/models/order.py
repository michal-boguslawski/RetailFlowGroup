from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from domain.enums import (
    StoreId, OrderEventType, Currency, OrderStatus
)
from domain.models.product import Product
from domain.models.promotion import Promotion
from domain.models.user import User


@dataclass
class OrderLineItem:
    product: Product
    id: int | None = None
    quantity: Optional[int] = None
    discount_pct: Optional[float] = None

    @staticmethod
    def _apply_discount(discount_pct: Optional[float], value: Decimal) -> Decimal:
        # print(self.product, type(self.product.price))
        discount_multiplier = (1 - discount_pct / 100) if discount_pct else 1
        return value * Decimal(discount_multiplier)

    @property
    def total_amount(self) -> Decimal:
        discounted_price = self._apply_discount(self.discount_pct, self.product.price)
        return discounted_price * (self.quantity or 1)

    @property
    def tax_amount(self) -> Decimal:
        discounted_tax = self._apply_discount(self.discount_pct, self.product.tax_amount)
        return discounted_tax * (self.quantity or 1)


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
    def tax_amount(self) -> Decimal:
        return sum((item.tax_amount for item in self.items), Decimal(0))


@dataclass
class OrderEvent:
    event_id: str
    event_type: OrderEventType
    event_ts: int
    store_id: StoreId
    order: Order
    failure_reason: Optional[str]


@dataclass
class GammaOrder:
    id: str
    user: User | None
    order_date: date
    status: OrderStatus
    products: list[Product]
    promotion: Promotion | None
    city: str
    currency: Currency
    discount_code: str = ""
    _shipping_cost: Decimal = Decimal(10)

    @property
    def total_amount(self) -> Decimal:
        gross_amount = Decimal(sum((p.price for p in self.products)))
        if self.promotion:
            if not self.promotion.is_free_shipping:
                gross_amount += self._shipping_cost

            gross_amount *= (1 - self.promotion.discount_percentage / 100)

            gross_amount -= self.promotion.discount_fixed

        return gross_amount
