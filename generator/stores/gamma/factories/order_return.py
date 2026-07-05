from datetime import date, datetime, timedelta
from faker import Faker

from domain.enums import ReasonCodePL, ReasonCodeDE, ConditionDE, ConditionPL, Country, OrderStatus
from domain.models.order import GammaOrder
from domain.models.order_return import OrderReturn
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory
from infrastructure.core.db_service import DBService


class GammaOrderReturnFactory(BaseFactory[OrderReturn]):
    def __init__(
        self,
        id_generator: IdGenerator,
        db_service: DBService,
        fake: Faker | None = None,
    ):
        self.fake = fake or make_faker()
        self.id_generator = id_generator
        self.db_service = db_service

    def make_one(self, date_: date) -> OrderReturn:
        order = self.db_service.get_random("orders", order_status = OrderStatus.ZREALIZOWANE)
        if not isinstance(order, GammaOrder):
            raise TypeError(f"order is not GammaOrder type, but {type(order)}")

        return_ts = (
            datetime.combine(date_, datetime.min.time())
            + timedelta(seconds=self.fake.random_int(min=0, max=86399))
        )

        country = self.fake.random_element([Country.DE, Country.PL])
        ReasonCode = ReasonCodePL if country == Country.PL else ReasonCodeDE
        Condition = ConditionPL if country == Country.PL else ConditionDE

        returned_items = self.fake.random_elements(
            elements=order.products,
            length=self.fake.random_int(min=1, max=len(order.products)),
            unique=True,
        )
        order.status = OrderStatus.ANULOWANE

        return OrderReturn(
            id = self.id_generator.make_id("return_id"),
            order = order,
            return_ts = return_ts,
            country = country,
            reason_code = self.fake.random_element(list(ReasonCode)),
            condition = self.fake.random_element(list(Condition)),
            items = returned_items,
        )
