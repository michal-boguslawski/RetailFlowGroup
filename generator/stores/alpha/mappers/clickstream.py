from domain.models import ClickstreamEvent
from schemas.clickstreams.alpha import ClickstreamEvent as AvroClickstreamEvent


def clickstream_to_avro(clickstream_event: ClickstreamEvent) -> AvroClickstreamEvent:
    user = clickstream_event.user
    return AvroClickstreamEvent(
        event_id=clickstream_event.event_id,
        event_type=clickstream_event.event_type.value,
        event_ts=clickstream_event.event_ts,
        received_ts=clickstream_event.received_ts,
        store_id=clickstream_event.store_id.value,
        session_id=clickstream_event.session_id,
        user_id=user.id if user else None,
        anonymous_id=clickstream_event.anonymous_id,
        product_id=clickstream_event.product_id,
        page_url=clickstream_event.page_url,
        device_type=clickstream_event.device_type.value if clickstream_event.device_type else None,
        ip_address=None if user and user.gdpr_consent else clickstream_event.ip_address,
        country_code=clickstream_event.country_code,
        ab_variant=clickstream_event.ab_variant,
        scroll_depth_pct=clickstream_event.scroll_depth_pct,
        schema_version=clickstream_event.schema_version
    )
