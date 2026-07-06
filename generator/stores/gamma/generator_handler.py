from datetime import date, timedelta
import random
from typing import Iterator

from domain.models import GammaOrder, GammaProduct, OrderReturn, Promotion, User
from domain.models.formatter import Formatter
from generator.stores.factory import StoreFactory
from infrastructure.core.db_service import DBService


class GammaEventHandler:
    def __init__(
        self,
        store_factory: StoreFactory,
        db_service: DBService,
        start_date: date = date(2023, 1, 1),
    ):
        self.db_service = db_service
        self.store_factory = store_factory
        self.start_date = start_date
        self.current_date = start_date

        # Iterator over products that must be emitted before anything else

        products = self.db_service.get_at_date("products", to_date = self.current_date)
        self._pending_products: Iterator[GammaProduct] = (
            p for p in products
            if isinstance(p, GammaProduct)
        )

    def _on_next_day(self) -> Formatter | None:
        self.current_date += timedelta(days=1)

        products = self.db_service.get_at_date("products", date_ = self.current_date)

        self._pending_products = (
            p for p in products
            if isinstance(p, GammaProduct)
        )
        if self.current_date.isoweekday == 7:
            formatter = self.store_factory.make_one("formatters", date_=self.current_date)
            if not isinstance(formatter, Formatter):
                raise TypeError
            return formatter

    def step(self) -> User | GammaOrder | GammaProduct | OrderReturn | Promotion | Formatter:
        # First emit any pending products
        try:
            return next(self._pending_products)
        except StopIteration:
            pass

        # Maybe advance to the next day
        if random.random() < 0.01:
            formatter = self._on_next_day()
            if formatter is not None:
                return formatter

            # If the new day has products, emit the first one immediately
            try:
                return next(self._pending_products)
            except StopIteration:
                pass

        # Otherwise generate a normal event
        return self._generate_random_event()

    def _generate_random_event(self) -> User | GammaOrder | OrderReturn | Promotion:
        event_name, event_model = random.choices([
            ("users", User),
            ("orders", GammaOrder),
            ("promotions", Promotion),
            ("order_returns", OrderReturn),
            ("end_promotion", None),
        ], weights=[2, 94, 1, 2, 1])[0]
        
        if event_name == "end_promotion" or event_model is None:
            promotion = self.db_service.get_random("promotions", date_=self.current_date)
            if not isinstance(promotion, Promotion):
                raise TypeError(
                    f"Expected Promotion, got {type(promotion)}"
                )
            promotion.valid_to = self.current_date
            return promotion
            
        
        event = self.store_factory.make_one(event_name, date_=self.current_date)
        
        if not isinstance(event, event_model):
            raise TypeError(
                f"Expected {event_model}, got {type(event)}"
            )
        
        # self.db_service.save(event_name, event)
        return event
