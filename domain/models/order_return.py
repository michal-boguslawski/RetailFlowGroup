from dataclasses import dataclass, field
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

    refund_amount: Decimal | None = field(init=False)

    def __post_init__(self):
        self.refund_amount = sum((i.price for i in self.items), Decimal("0"))

    @property
    def user(self) -> User | None:
        return self.order.user

    @property
    def return_id(self) -> str:
        return self.id.replace(
            "YYYYMMDD",
            self.return_ts.strftime("%Y%m%d"),
        )
