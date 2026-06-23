from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from domain.enums import (
    ClickstreamEventType, StoreId, OrderEventType, Currency, LoyaltyTier, AcquisitionChannel, DeviceType
)


@dataclass
class ClickstreamEvent:
    event_id: str
    event_type: ClickstreamEventType
    event_ts: int
    received_ts: int
    store_id: StoreId
    session_id: Optional[str]
    user: Optional["User"]
    anonymous_id: str
    product: Optional["Product"]
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


@dataclass
class Order:
    id: str
    user: Optional["User"]
    guest_email: Optional[str]
    items: list["OrderLineItem"]
    currency: Currency
    notes: Optional[str]

    @property
    def total_amount(self) -> Decimal:
        return sum((item.total_amount for item in self.items), Decimal(0))

    @property
    def tax_amount(self) -> Optional[Decimal]:
        if self.total_amount:
            return self.total_amount * Decimal(0.23)  # Assuming 23% tax rate


@dataclass
class OrderEvent:
    event_id: str
    event_type: OrderEventType
    event_ts: int
    store_id: StoreId
    order: Order
    failure_reason: Optional[str]
    schema_version: str


@dataclass
class User:
    id: str
    email: str
    phone: Optional[str]
    first_name: Optional[str]
    date_of_birth: Optional[date]
    loyalty_tier: LoyaltyTier
    acquisition_channel: Optional[AcquisitionChannel]
    gdpr_consent: bool
    legacy_customer_no: Optional[int]


@dataclass
class Product:
    id: str
    name: str
    price: Decimal
    category_path: str
    stock_count: Optional[int] = None
    ean_barcode: Optional[str] = None
    active: Optional[bool] = None
    tax_pc: Optional[Decimal] = None
    avg_rating: Optional[float] = None
    currency: Optional[Currency] = None


@dataclass
class OrderLineItem:
    product: Product
    id: int | None = None
    quantity: Optional[int] = None
    discount_pct: Optional[float] = None

    @property
    def total_amount(self) -> Decimal:
        # print(self.product, type(self.product.price))
        discount_multiplier = (1 - self.discount_pct / 100) if self.discount_pct else 1
        return self.product.price * (self.quantity or 1) * Decimal(discount_multiplier)
