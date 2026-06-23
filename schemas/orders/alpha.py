from dataclasses import dataclass, field
from typing import Optional, Literal
from dataclasses_avroschema import AvroModel


@dataclass
class OrderLineItem(AvroModel):
    """
    Single line item within an order.
    """

    product_id: str = field(
        metadata={
            "description": (
                "Store-local product identifier."
            )
        }
    )

    discount_pct: Optional[float] = field(
        default=None,
        metadata={
            "description": (
                "Discount applied to this line item. "
            )
        },
    )


@dataclass
class OrderEvent(AvroModel):
    """
    Order lifecycle event produced by retail stores alpha and beta.

    Schema divergence between stores is significant — consumers must
    branch on store_id and schema_version to handle field renames,
    missing fields, and incompatible value encodings.
    """

    event_id: str = field(
        metadata={
            "description": (
                "Event identifier."
                "Not guaranteed unique across stores."
            )
        }
    )

    event_type: Literal[
        "order_created",
        "payment_initiated",
        "payment_confirmed",
        "payment_failed",
        "shipped",
        "delivered",
        "return_requested",
        "refunded",
        "cancelled",
    ] = field(
        metadata={
            "description": (
                "Event type discriminator: "
                "order_created | payment_initiated | payment_confirmed | payment_failed | "
                "shipped | delivered | return_requested | refunded | cancelled"
            )
        }
    )

    event_ts: int = field(
        metadata={
            "description": (
                "Event timestamp in Unix epoch millis. "
                "Server-side on alpha (reliable). Client-side on beta (may drift)."
            )
        }
    )

    order_id: str = field(
        metadata={
            "description": (
                "Store-local order identifier."
            )
        }
    )

    currency: Literal[
        "PLN",
        "EUR",
        "GBP",
    ] = field(
        metadata={
            "description": (
                "ISO 4217 currency code."
                "PLN | EUR | GBP"
            )
        }
    )

    schema_version: str = field(
        default="2.1.0",
        metadata={
            "description": (
                "Schema version string."
            )
        }
    )

    store_id: str = field(
        default="alpha",
        metadata={
            "description": (
                "'alpha' or 'beta'. Critical for order_id namespacing — "
                "IDs are sequential integers in both stores and will collide."
            )
        }
    )

    user_id: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "Authenticated user identifier. Null for guest checkouts "
            )
        },
    )

    guest_email: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "Guest checkout email in plain text."
            )
        },
    )

    total_amount: Optional[float] = field(
        default=None,
        metadata={
            "description": (
                "Order total in `currency` units. Null on non-financial events "
            )
        },
    )

    tax_amount: Optional[float] = field(
        default=None,
        metadata={
            "description": (
                "Tax component of total_amount. Null when calculated at fulfilment. "
            )
        },
    )

    failure_reason: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "Free-text failure description. Present only on payment_failed and cancelled events. "
                "Values are inconsistent across stores — do not rely on exact strings."
            )
        },
    )

    items: list[OrderLineItem] = field(
        default_factory=list,
        metadata={
            "description": (
                "Line items for this order. Empty list on non-order events. "
            )
        },
    )

    class Meta:
        namespace = "com.retailflow.order"
