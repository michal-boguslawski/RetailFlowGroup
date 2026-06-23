from dataclasses import asdict
from typing import Any

from domain.models import OrderEvent
from schemas.orders.beta import OrderEvent as AvroOrderEvent
from schemas.orders.beta import OrderLineItem as AvroOrderLineItem


def beta_order_renderer(event: OrderEvent, ctx) -> dict[str, Any]:
    items = [
        AvroOrderLineItem(item.product.id, item.discount_pct)
        for item in event.order.items
    ]
    avro_event = AvroOrderEvent(
        event_id=event.event_id,
        event_type=event.event_type.value,
        event_ts=event.event_ts,
        order_id=event.order.id,
        currency=event.order.currency.value,
        schema_version=event.schema_version,
        store_id=event.store_id,
        user_id=event.order.user.id if event.order.user else None,
        totalPrice=float(event.order.total_amount),
        failure_reason=event.failure_reason,
        lineItems=items,
    )
    return asdict(avro_event)
    