from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from domain.enums import (
    ReasonCodePL, ReasonCodeDE, ConditionPL, ConditionDE, Country
)
from domain.models.order import GammaOrder
from domain.models.product import Product
from domain.models.user import User


@dataclass
class OrderReturn:
    id: str
    order: GammaOrder
    return_ts: datetime
    country: Country
    reason_code: ReasonCodePL | ReasonCodeDE
    condition: ConditionPL | ConditionDE
    items: Sequence[Product]

    @property
    def user(self) -> User | None:
        return self.order.user

    @property
    def refund_amount(self) -> Decimal:
        return sum((i.price for i in self.items), Decimal(0))
