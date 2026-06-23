from enum import StrEnum


class OrderEventType(StrEnum):
    ORDER_CREATED       = "order_created"
    PAYMENT_INITIATED   = "payment_initiated"
    PAYMENT_CONFIRMED   = "payment_confirmed"
    PAYMENT_FAILED      = "payment_failed"
    SHIPPED             = "shipped"
    DELIVERED           = "delivered"
    RETURN_REQUESTED    = "return_requested"
    REFUNDED            = "refunded"
    CANCELLED           = "cancelled"

    def is_financial(self) -> bool:
        return self in {
            self.PAYMENT_INITIATED,
            self.PAYMENT_CONFIRMED,
            self.PAYMENT_FAILED,
            self.REFUNDED,
        }


class ClickstreamEventType(StrEnum):
    PAGE_VIEW           = "page_view"
    PRODUCT_VIEW        = "product_view"
    ADD_TO_CART         = "add_to_cart"
    REMOVE_FROM_CART    = "remove_from_cart"
    CHECKOUT_START      = "checkout_start"
    CHECKOUT_ABANDON    = "checkout_abandon"


class DeviceType(StrEnum):
    DESKTOP     = "desktop"
    MOBILE      = "mobile"
    TABLET      = "tablet"
    UNKNOWN     = "unknown"


class LoyaltyTier(StrEnum):
    STANDARD    = "standard"
    SILVER      = "silver"
    GOLD        = "gold"
    VIP         = "vip"


class Currency(StrEnum):
    PLN = "PLN"
    EUR = "EUR"
    GBP = "GBP"


class StoreId(StrEnum):
    ALPHA   = "alpha"
    BETA    = "beta"
    GAMMA   = "gamma"


class AcquisitionChannel(StrEnum):
    ORGANIC     = "organic"
    PAID_SEARCH = "paid_search"
    REFERRAL    = "referral"
    SOCIAL      = "social"


class EntityType(StrEnum):
    ORDERS       = "orders"
    USERS        = "users"
    PRODUCTS     = "products"
    CLICKSTREAMS = "clickstreams"


class ExitEventType(StrEnum):
    EXIT = "exit"
