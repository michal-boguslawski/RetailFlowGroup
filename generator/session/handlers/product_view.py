from dataclasses import dataclass
from typing import Literal

from domain.enums import ClickstreamEventType
from domain.models import ClickstreamEvent, Product
from generator.session.handler_registry import handler
from generator.session.handlers.base import ClickstreamTransitionHandler
from generator.session.state import Session
from infrastructure.core.db_service import DBService


@handler(ClickstreamEventType.PRODUCT_VIEW)
class ProductViewHandler(ClickstreamTransitionHandler[ClickstreamEventType.PRODUCT_VIEW]):
    def __init__(
        self,
        expected_event_type: Literal[ClickstreamEventType.PRODUCT_VIEW],
        db_service: DBService,
        *args,
        **kwargs
    ):
        super().__init__(expected_event_type, *args, **kwargs)
        self.expected_event_type = expected_event_type
        self.db_service = db_service

    def _post_handle(self, session: Session) -> ClickstreamEvent:
        assert session.clickstream_event is not None

        product = self.db_service.get_random("products")
        # print(f"Got random product: {product}")
        assert isinstance(product, Product), (
            f"Random product must be a Product, but is {type(product)}"
        )
        session.clickstream_event.product = product
        return session.clickstream_event
