from dataclasses import dataclass
from typing import Optional

from domain.enums import (
    ClickstreamEventType, StoreId, DeviceType
)
from domain.models.user import User
from domain.models.product import Product


@dataclass
class ClickstreamEvent:
    event_id: str
    event_type: ClickstreamEventType
    event_ts: int
    received_ts: int
    store_id: StoreId
    session_id: Optional[str]
    user: Optional[User]
    anonymous_id: str
    product: Optional[Product]
    # page_url: Optional[str]
    device_type: Optional[DeviceType]
    ip_address: Optional[str]
    country_code: Optional[str]
    ab_variant: Optional[str]
    scroll_depth_pct: Optional[float]
    schema_version: str
    new: bool = True

    @property
    def page_url(self):
        base_url = f"https://{self.store_id.value}.com"
        product_id = self.product.id if self.product else None
        if self.event_type == ClickstreamEventType.PAGE_VIEW:
            return base_url
        elif self.event_type == ClickstreamEventType.PRODUCT_VIEW and product_id:
            return f"{base_url}/product/{product_id}"
        elif product_id:
            return f"{base_url}/product/{product_id}?event={self.event_type.value}"
        else:
            return f"{base_url}/{self.event_type.value}"
