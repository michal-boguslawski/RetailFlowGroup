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

    def is_mobile(self):
        return self in {
            self.MOBILE,
            self.TABLET,
        }


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


class Country(StrEnum):
    PL = "PL"
    DE = "DE"
    GB = "GB"


class PrefferedLanguages(StrEnum):
    PL = "pl"
    EN = "en"


class DiscountTypesEN(StrEnum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    FREE_SHIPPING = "free_shipping"
    BOGO = "bogo"


class DiscountTypesPL(StrEnum):
    PERCENTAGE = "procentowy"
    FIXED = "stawka stała"
    FREE_SHIPPING = "darmowa dostawa"
    BOGO = "kup jedno, drugie w gratisie"


class OrderStatus(StrEnum):
    ZREALIZOWANE = "zrealizowane"
    ANULOWANE = "anulowane"
    W_TRAKCIE = "w trakcie"


class ReasonCodePL(StrEnum):
    DEFECT = "DEF"
    SIZE = "SIZ"
    EXCHANGE = "CHG"
    SHIPPING_DAMAGE = "DAM"


class ReasonCodeDE(StrEnum):
    DEFECT = "DEFEKT"
    SIZE = "GROESSE"
    SHIPPING_DAMAGE = "TRANSPORT"


class ConditionPL(StrEnum):
    NEW = "NEW"
    DAMAGED = "DAMAGED"
    USED = "USED"


class ConditionDE(StrEnum):
    NEW = "A"
    DAMAGED = "B"
    USED = "C"
    REFURBISHED = "D"


class OffsetWriter(StrEnum):
    BATCH = "batch"
    STREAMING = "streaming"


COUNTRY_CURRENCY_MAP = {
    Country.PL: Currency.PLN,
    Country.DE: Currency.EUR,
    Country.GB: Currency.GBP,
}


def get_currency(country: Country) -> Currency:
    return COUNTRY_CURRENCY_MAP[country]
