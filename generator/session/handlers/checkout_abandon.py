from domain.enums import ClickstreamEventType
from domain.models import ClickstreamEvent
from generator.session.handler_registry import handler
from generator.session.handlers.base import ClickstreamTransitionHandler
from generator.session.state import Session


@handler(ClickstreamEventType.CHECKOUT_ABANDON)
class CheckoutAbandonHandler(ClickstreamTransitionHandler[ClickstreamEventType.CHECKOUT_ABANDON]):

    def _post_handle(self, session: Session) -> ClickstreamEvent:
        assert session.clickstream_event is not None
        session.clickstream_event.product = None
        return session.clickstream_event
