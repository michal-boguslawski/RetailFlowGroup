from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from domain.enums import DiscountTypesPL, DiscountTypesEN, Currency


@dataclass
class Promotion:
    promo_code: str
    discount_value: Decimal
    valid_from: date
    valid_to: date | None
    min_order_value: Decimal
    discount_type: DiscountTypesPL | DiscountTypesEN
    currency: Currency

    @property
    def discount_percentage(self) -> Decimal:
        return (
            Decimal(0.0) if self.discount_type not in (DiscountTypesPL.PERCENTAGE, DiscountTypesEN.PERCENTAGE) else self.discount_value
        )

    @property
    def discount_fixed(self) -> Decimal:
        return (
            Decimal(0.0) if self.discount_type not in (DiscountTypesPL.FIXED, DiscountTypesEN.FIXED) else self.discount_value
        )

    @property
    def is_free_shipping(self) -> bool:
        return self.discount_type in (DiscountTypesEN.FREE_SHIPPING, DiscountTypesPL.FREE_SHIPPING)

    def is_active(self, val_date: date) -> bool:
        if val_date < self.valid_from:
            return False

        if self.valid_to and val_date > self.valid_to:
            return False

        return True

    def is_applicable(self, amount: Decimal) -> bool:
        return amount >= self.min_order_value
        