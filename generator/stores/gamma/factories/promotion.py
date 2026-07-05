from datetime import date
from decimal import Decimal
from faker import Faker

from domain.enums import Country, DiscountTypesEN, DiscountTypesPL, get_currency
from domain.models.promotion import Promotion
from generator.core.fake import make_faker
from generator.stores.base import BaseFactory


PROMO_CODES_PREFIXES = {
    DiscountTypesEN.PERCENTAGE: ["SAVE", "OFF", "PCT", "WELCOME"],
    DiscountTypesEN.FIXED: ["FLAT", "TAKE", "CASH", "SAVEFIX"],
    DiscountTypesEN.FREE_SHIPPING: ["FREE", "SHIP", "DELIVER"],
    DiscountTypesEN.BOGO: ["BOGO", "BUY", "GET"],
    DiscountTypesPL.PERCENTAGE: ["OSZCZEDZ", "RABAT", "PRO", "WITAJ"],
    DiscountTypesPL.FIXED: ["FLAT", "ZNIŻKA", "STAŁY", "KASZA"],
    DiscountTypesPL.FREE_SHIPPING: ["BEZPŁATNA", "DOSTAWA", "WYSYŁKA"],
    DiscountTypesPL.BOGO: ["KUPJEDNO", "DARUJ", "ZLIZA", "KUP1"],
}


DISCOUNT_RULES = {
    DiscountTypesEN.PERCENTAGE: {"min": 5, "max": 30},
    DiscountTypesEN.FIXED: {"min": 5, "max": 100},
    DiscountTypesPL.PERCENTAGE: {"min": 5, "max": 30},
    DiscountTypesPL.FIXED: {"min": 5, "max": 100},
}


def get_season(month: int) -> str:
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        raise ValueError("month must be 1-12")


class GammaPromotionFactory(BaseFactory[Promotion]):
    def __init__(
        self,
        fake: Faker | None = None
    ):
        self.fake = fake or make_faker()

    def _generate_discount_value(self, discount_type: DiscountTypesEN | DiscountTypesPL) -> Decimal:
        if discount_type in DISCOUNT_RULES:
            rule = DISCOUNT_RULES[discount_type]
            return Decimal(self.fake.random_int(rule["min"], rule["max"], step=5))

        return Decimal(0)

    def _generate_min_order_value(self, discount_type: DiscountTypesEN | DiscountTypesPL, discount_value: Decimal) -> Decimal:
        if discount_type in (DiscountTypesEN.FREE_SHIPPING, DiscountTypesEN.BOGO, DiscountTypesPL.FREE_SHIPPING, DiscountTypesPL.BOGO):
            return Decimal(self.fake.random_int(100, 500, 50))
        return discount_value * self.fake.random_int(5, 10)

    def _generate_promo_code(self, discount_type: DiscountTypesEN | DiscountTypesPL, discount_value: Decimal, valid_from: date) -> str:
        prefix = self.fake.random_element(PROMO_CODES_PREFIXES[discount_type])
        season = get_season(valid_from.month).upper()
        year = valid_from.year
        promo_code = prefix
        if self.fake.boolean():
            promo_code += f"_{season}"
        if self.fake.boolean():
            promo_code += str(year)
        if discount_type in (DiscountTypesEN.PERCENTAGE, DiscountTypesEN.FIXED, DiscountTypesPL.PERCENTAGE, DiscountTypesPL.FIXED):
            promo_code += f"{discount_value}"
        return promo_code

    def make_one(self, date_: date) -> Promotion:
        country = self.fake.random_element([Country.PL, Country.DE])
        currency = get_currency(country)
        discount_types = (
            list(DiscountTypesPL)
            if country == Country.PL
            else list(DiscountTypesEN)
        )
        discount_type = self.fake.random_element(discount_types)
        discount_value = self._generate_discount_value(discount_type)
        return Promotion(
            promo_code=self._generate_promo_code(discount_type, discount_value, date_),
            discount_value=discount_value,
            valid_from=date_,
            valid_to=None,
            min_order_value=self._generate_min_order_value(discount_type, discount_value),
            discount_type=discount_type,
            currency=currency,
        )
