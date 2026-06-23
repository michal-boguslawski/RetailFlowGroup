from domain.enums import OrderEventType
from domain.models import OrderEvent
from generator.session.handler_registry import handler
from generator.session.handlers.base import OrderTransitionHandler
from generator.session.state import Session


@handler(OrderEventType.SHIPPED)
class ShippedHandler(OrderTransitionHandler[OrderEventType.SHIPPED]):

    def _post_handle(self, session: Session) -> OrderEvent:
        assert session.order_event is not None
        return session.order_event
