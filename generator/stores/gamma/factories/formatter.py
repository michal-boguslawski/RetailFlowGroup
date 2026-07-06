from datetime import date
from decimal import Decimal
from faker import Faker
from typing import Callable

from domain.models.order import GammaOrder
from domain.models.promotion import Promotion
from domain.models.formatter import Formatter, ColumnNamingVariant
from generator.core.fake import make_faker
from generator.stores.base import BaseFactory


DATE_FORMATTERS: list[Callable[[date], str]] = [
    lambda d: d.strftime("%Y-%m-%d"),
    lambda d: d.strftime("%d/%m/%Y"),
    lambda d: d.strftime("%m-%d-%Y"),
    lambda d: d.strftime("%d %b %Y"),  # e.g. "15 Jan 2024"
]


AMOUNT_FORMATTERS: list[Callable[[GammaOrder], str]] = [
    lambda o: f"{o.total_amount:.2f}",
    lambda o: f"{o.total_amount:.2f}",
    lambda o: f"{o.currency.value}{o.total_amount:.2f}",
    lambda o: f"{o.total_amount:.2f} {o.currency.value}",
]


MIN_ORDER_VALUE_FORMATTERS: list[Callable[[Promotion], str]] = [
    lambda o: str(o.min_order_value),
    lambda o: f"{o.min_order_value:.2f}",
    lambda o: f"{o.currency.value}{o.min_order_value:.2f}",
    lambda o: f"{o.min_order_value} {o.currency.value}",
]


DISCOUNT_VALUE_FORMATTERS: list[Callable[[Decimal], Decimal]] = [
    lambda o: o,
    lambda o: o / 100,
]


TOTALS_GENERATOR_FORMATTERS: list[Callable[[list[Promotion]], str]] = [
    lambda ps: f"Total,{len(ps)}",
]


class GammaFormatterFactory(BaseFactory[Formatter]):
    def __init__(self, fake: Faker | None = None):
        self.fake = fake or make_faker()

    def make_one(self, date_: date, *args, **kwargs) -> Formatter:
        return Formatter(
            current_date=date_,
            order_date_formattter_fn=self.fake.random_element(DATE_FORMATTERS),
            amount_formatter_fn=self.fake.random_element(AMOUNT_FORMATTERS),
            discount_value_formatter_fn=self.fake.random_element(
                DISCOUNT_VALUE_FORMATTERS
            ),
            valid_formatter_fn=self.fake.random_element(DATE_FORMATTERS),
            min_order_value_formatter_fn=self.fake.random_element(
                MIN_ORDER_VALUE_FORMATTERS
            ),
            totals_generator_fn=self.fake.random_element(
                    TOTALS_GENERATOR_FORMATTERS
            ),
            column_naming_variants=ColumnNamingVariant(
                order_id=self.fake.random_element(["order_id", "OrderID", "order_no", "ID"]),
                user_id=self.fake.random_element(["user_id", "CustomerID", "cust_id", "user"]),
                order_date=self.fake.random_element(["order_date", "Date", "OrderDate", "data"]),
                total_amount=self.fake.random_element(["total_amount", "Total", "Amount", "Kwota", "TotalPLN"]),
                status=self.fake.random_element(["status", "Status", "OrderStatus", "stan"]),
                product_ids=self.fake.random_element(["product_ids", "Products", "items", "ProductList"]),
                discount_code=self.fake.random_element(["discount_code", "Promo", "PromoCode", "rabat"]),
                city=self.fake.random_element(["city", "City", "Miasto", "shipping_city"]),
                promo_code=self.fake.random_element(["promo_code", "PromoCode", "code", "PROMO_CODE", "Promo Code"]),
                discount_value=self.fake.random_element(["discount_value", "Discount%", "discount", "disc_pct", "Rabat"]),
                valid_from=self.fake.random_element(["valid_from", "start_date", "StartDate", "from", "od"]),
                valid_to=self.fake.random_element(["valid_to", "end_date", "EndDate", "to", "expiry", "do"]),
                min_order_value=self.fake.random_element(["min_order_value", "MinOrder", "min_cart", "Minimalna"]),
                discount_type=self.fake.random_element(["discount_type", "Type", "DiscountType", "rodzaj"]),
            ),
        )

        
