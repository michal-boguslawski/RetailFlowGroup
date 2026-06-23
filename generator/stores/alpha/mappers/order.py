from dataclasses import asdict
from typing import Any

from domain.models import OrderEvent
from generator.schemas.orders.alpha import OrderEvent as AvroOrderEvent
from generator.schemas.orders.alpha import OrderLineItem as AvroOrderLineItem


def order_renderer(event: OrderEvent, ctx) -> dict[str, Any]:
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
        guest_email=event.order.guest_email,
        total_amount=round(float(event.order.total_amount), 2),
        tax_amount=round(float(event.order.tax_amount), 2) if event.order.tax_amount else None,
        failure_reason=event.failure_reason,
        items=items,
    )
    return asdict(avro_event)
