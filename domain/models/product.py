from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from domain.enums import Currency


@dataclass
class PriceEntry:
    """One per-country price point on a Beta product. Modern-shape only —
    legacy Beta docs flatten this down to a single price + currency."""
    country: str
    currency: str
    amount: Decimal
    vat_rate: Decimal


@dataclass
class ProductVariant:
    sku: str
    color: str
    size: str
    stock: int


@dataclass
class StockDetail:
    """Modern Beta stock shape. Legacy docs use a flat integer instead."""
    total: int
    reserved: int
    warehouses: dict[str, int] = field(default_factory=dict)


@dataclass
class Product(ABC):
    """Canonical base. Only fields every store genuinely shares live here —
    category_path and price are deliberately excluded; each store's shape
    for those concepts diverges too much (type, cardinality, or both) to
    force into a shared field. See AlphaProduct / BetaProduct."""

    id: str
    name: str

    @property
    @abstractmethod
    def net_price(self) -> Decimal:
        ...

    @property
    @abstractmethod
    def tax_amount(self) -> Decimal:
        """Tax amount, derived from price and tax rate. Not stored; computed
        on-the-fly. Zero if tax_pc is not set."""
        ...

    @property
    def price(self) -> Decimal:
        """Every Product must expose a single canonical price, however it's
        derived. Stored field on Alpha; computed from price_entries on Beta."""
        return self.net_price + self.tax_amount


@dataclass
class AlphaProduct(Product):
    _price: Decimal = Decimal("0")
    category_path: str = ""
    tax_pc: Optional[Decimal] = None
    currency: Optional[Currency] = None

    @property
    def net_price(self) -> Decimal:
        return self._price

    @net_price.setter
    def net_price(self, value: Decimal) -> None:
        self._price = value

    @property
    def tax_amount(self) -> Decimal:
        if self.tax_pc is None:
            return Decimal("0")
        return self.net_price * (self.tax_pc / 100)


@dataclass
class BetaProduct(Product):
    category_path: list[str] = field(default_factory=list)
    legacy_shape: bool = False
    price_entries: list[PriceEntry] = field(default_factory=list)
    stock_detail: StockDetail | None = None
    status: bool = True
    variants: list[ProductVariant] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    avg_rating: Optional[float] = None

    @property
    def net_price(self) -> Decimal:
        if not self.price_entries:
            return Decimal("0")
        return self.price_entries[0].amount

    @property
    def category(self) -> str:
        """Legacy flat representation, derived from the canonical hierarchy.
        Used by the mapper when legacy_shape=True. Currently takes the leaf
        category; change to '/'.join(self.category_path) if your reference
        legacy shape used a joined path instead."""
        if not self.category_path:
            return ""
        return '/'.join(self.category_path)

    @property
    def tax_amount(self) -> Decimal:
        if not self.price_entries:
            return Decimal("0")
        price_entry = self.price_entries[0]
        return self.net_price * (price_entry.vat_rate / 100)


@dataclass
class GammaProduct(Product):
    category: str
    _price: Decimal
    stock_count: int
    ean_barcode: str
    active: int
    created_date: str

    @property
    def net_price(self) -> Decimal:
        return self._price

    @net_price.setter
    def net_price(self, value: Decimal) -> None:
        self._price = value

    @property
    def tax_amount(self) -> Decimal:
        return self.net_price * Decimal(0.23)
