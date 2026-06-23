from faker import Faker
from typing import Optional

from domain.models import OrderEvent, Order, OrderLineItem, User
from domain.enums import OrderEventType, StoreId, Currency
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory


class AlphaOrderFactory(BaseFactory[OrderEvent]):
    def __init__(
        self,
        id_generator: IdGenerator,
        fake: Optional[Faker] = None,
        clock_drift_seconds: int = 0,
    ):
        self.fake = fake or make_faker()
        self.id_generator = id_generator
        self.clock_drift_seconds = clock_drift_seconds

    def make_one(self, user: User, items: list[OrderLineItem], event_ts: int) -> OrderEvent:
        order = Order(
            id=self.id_generator.make_id("order_id"),
            user=user,
            guest_email=self.fake.email(),
            items=items,
            currency=self.fake.random_element(list(Currency)),
            notes=None
        )

        return OrderEvent(
            event_id=self.id_generator.make_id("order_event_id"),
            event_type=OrderEventType.ORDER_CREATED,
            event_ts=event_ts,
            store_id=StoreId.ALPHA,
            order=order,
            failure_reason=None,
            schema_version="2.1.0"
        )
