from dataclasses import dataclass, field

from domain.types import EventType
from domain.models import OrderLineItem, ClickstreamEvent, OrderEvent


@dataclass
class Session:
    current_state: EventType | None = None
    cart: list[OrderLineItem] = field(default_factory=list)
    clickstream_event: ClickstreamEvent | None = None
    order_event: OrderEvent | None = None
