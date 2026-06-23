from domain.enums import ClickstreamEventType
from domain.models import ClickstreamEvent, Product, OrderLineItem
from generator.session.handler_registry import handler
from generator.session.handlers.base import ClickstreamTransitionHandler
from generator.session.state import Session


@handler(ClickstreamEventType.ADD_TO_CART)
class AddToCartHandler(ClickstreamTransitionHandler[ClickstreamEventType.ADD_TO_CART]):

    def _post_handle(self, session: Session) -> ClickstreamEvent:

        assert session.clickstream_event is not None
        product = session.clickstream_event.product
        assert type(product) is Product, "Random product must be of type Product"
        session.cart.append(
            OrderLineItem(
                product=product,
                quantity=1
            )
        )
        return session.clickstream_event
