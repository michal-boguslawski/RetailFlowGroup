# schemas/models/clickstream.py

from dataclasses import dataclass, field
from typing import Optional, Literal
from dataclasses_avroschema import AvroModel


@dataclass
class ClickstreamEvent(AvroModel):
    """
    Raw clickstream event produced by frontend tracking.

    These events are semi-structured and may have missing fields depending on:
    - browser capabilities
    - consent/GDPR flags
    - session initialization state
    - client-side retries or network conditions
    """

    event_id: str = field(
        metadata={
            "description": "UUID v4 generated client-side. Not guaranteed unique due to retries."
        }
    )

    event_type: Literal[
        "page_view",
        "product_view",
        "add_to_cart",
        "remove_from_cart",
        "checkout_start",
        "checkout_abandon",
    ] = field(
        metadata={
            "description": (
                "Event type discriminator: "
                "page_view | product_view | add_to_cart | "
                "remove_from_cart | checkout_start | checkout_abandon"
            )
        }
    )

    event_ts: int = field(
        metadata={
            "description": "Client-side event timestamp in Unix epoch millis (may drift)."
        }
    )

    received_ts: int = field(
        metadata={
            "description": "Server ingestion timestamp in millis. Preferred for ordering."
        }
    )

    anonymous_id: str = field(
        metadata={
            "description": "Stable anonymous identifier used to stitch sessions pre-login."
        }
    )

    store_id: str = field(
        default="beta",
        metadata={
            "description": (
                "Store name injected by ingestion layer"
            )
        }
    )

    session_id: Optional[str] = field(
        default=None,
        metadata={"description": "Session identifier. Null if cookies disabled or session not initialized."},
    )

    user_id: Optional[str] = field(
        default=None,
        metadata={"description": "Authenticated user ID. Null for anonymous traffic."},
    )

    product_id: Optional[str] = field(
        default=None,
        metadata={"description": "Product identifier. Only set for product-related events."},
    )

    search_query: Optional[str] = field(
        default=None,
        metadata={
            "description": "Raw user search query. May contain PII, typos, or unsafe input."
        },
    )

    page_url: Optional[str] = field(
        default=None,
        metadata={"description": "Full page URL including query params (web only)."},
    )

    device_type: Optional[
        Literal["desktop", "mobile", "tablet", "unknown"]
    ]= field(
        default=None,
        metadata={"description": "Device category: desktop | mobile | tablet | unknown"},
    )

    ip_address: Optional[str] = field(
        default=None,
        metadata={
            "description": "IP address (IPv4/IPv6). Must be anonymized before downstream storage."
        },
    )

    country_code: Optional[str] = field(
        default=None,
        metadata={
            "description": "ISO 3166-1 alpha-2 country code derived from IP geolocation."
        },
    )

    scroll_depth_pct: Optional[float] = field(
        default=None,
        metadata={
            "description": "Scroll depth percentage (0-100). Web only; null for native apps."
        },
    )

    ab_variant: Optional[str] = field(
        default=None,
        metadata={"description": "A/B test bucket assignment. Null if no experiment assigned."},
    )

    schema_version: Optional[str] = field(
        default=None,
        metadata={"description": "Schema version for backward compatibility tracking."},
    )

    class Meta:
        namespace = "com.retailflow.clickstream"
