from dataclasses import asdict
from typing import Any

from domain.models import ClickstreamEvent
from schemas.clickstreams.beta import ClickstreamEvent as AvroClickstreamEvent

def beta_clickstream_renderer(event: ClickstreamEvent, ctx) -> dict[str, Any]:
    avro_event = AvroClickstreamEvent(
        event_id=event.event_id,
        event_type=event.event_type.value,
        event_ts=event.event_ts,
        received_ts=event.received_ts,
        anonymous_id=event.anonymous_id,
        store_id=event.store_id,
        session_id=event.session_id,
        user_id=event.user.id if event.user else None,
        product_id=event.product.id if event.product else None,
        page_url=event.page_url,
        device_type=event.device_type.value if event.device_type else None,
        ip_address=event.ip_address,
        country_code=event.country_code,
        scroll_depth_pct=event.scroll_depth_pct,
        ab_variant=event.ab_variant,
        schema_version=None,
    )
    return asdict(avro_event)
    