from domain.enums import ClickstreamEventType
from domain.models import ClickstreamEvent, Product
from generator.session.handler_registry import handler
from generator.session.handlers.base import ClickstreamTransitionHandler
from generator.session.state import Session


@handler(ClickstreamEventType.REMOVE_FROM_CART)
class RemoveFromCartHandler(ClickstreamTransitionHandler[ClickstreamEventType.REMOVE_FROM_CART]):

    def _post_handle(self, session: Session) -> ClickstreamEvent:
        assert session.clickstream_event is not None
        product = session.clickstream_event.product
        assert isinstance(product, Product), (
            f"Random product must be a Product, but is {type(product)}"
        )
        for item in session.cart:
            if item.product is product:
                session.cart.remove(item)
                break
        return session.clickstream_event
