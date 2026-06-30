from typing import Literal

from domain.enums import OrderEventType
from domain.models import OrderEvent
from generator.session.handler_registry import handler
from generator.session.handlers.base import TransitionHandler
from generator.session.state import Session
from generator.stores.factory import StoreFactory


@handler(OrderEventType.ORDER_CREATED)
class OrderCreatedHandler(TransitionHandler[OrderEventType.ORDER_CREATED]):
    def __init__(
        self,
        expected_event_type: Literal[OrderEventType.ORDER_CREATED],
        store_factory: StoreFactory,
        *args,
        **kwargs
    ):
        super().__init__(
            expected_event_type, *args, **kwargs
        )
        self.store_factory = store_factory

    def handle(self, session: Session) -> OrderEvent:
        assert session.clickstream_event is not None, "Session must have a clickstream event"

        order_event = self.store_factory.make_one(
            "orders",
            user=session.clickstream_event.user,
            items=session.cart.copy(),
            event_ts=session.clickstream_event.event_ts
        )
        assert type(order_event) is OrderEvent, "Random order event must be of type OrderEvent"
        session.clickstream_event.product = None
        session.current_state = self.expected_event_type
        session.cart.clear()
        session.order_event = order_event
        return order_event
