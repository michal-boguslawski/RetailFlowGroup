from domain.models import OrderEvent
from schemas.orders.alpha import OrderEvent as AvroOrderEvent
from schemas.orders.alpha import OrderLineItem as AvroOrderLineItem


def order_event_to_avro(order_event: OrderEvent) -> AvroOrderEvent:
    return AvroOrderEvent(
        event_id=order_event.event_id,
        event_type=order_event.event_type.value,
        event_ts=order_event.event_ts,
        store_id=order_event.store_id.value,
        order_id=order_event.order.id,
        user_id=order_event.order.user.id if order_event.order.user else None,
        guest_email=order_event.order.guest_email,
        currency=order_event.order.currency.value,
        total_amount=order_event.order.total_amount,
        tax_amount=order_event.order.tax_amount,
        items=[AvroOrderLineItem(
            product_id=item.product.id,
            discount_pct=item.discount_pct
        ) for item in order_event.order.items],
        failure_reason=order_event.failure_reason,
        schema_version=order_event.schema_version
    )
