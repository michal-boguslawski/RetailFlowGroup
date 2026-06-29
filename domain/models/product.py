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
    def price(self) -> Decimal:
        """Every Product must expose a single canonical price, however it's
        derived. Stored field on Alpha; computed from price_entries on Beta."""
        ...


@dataclass
class AlphaProduct(Product):
    _price: Decimal = Decimal("0")
    category_path: str = ""
    tax_pc: Optional[Decimal] = None
    currency: Optional[Currency] = None

    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value: Decimal) -> None:
        self._price = value


@dataclass
class BetaProduct(Product):
    category_path: list[str] = field(default_factory=list)
    legacy_shape: bool = False
    price_entries: list[PriceEntry] = field(default_factory=list)
    stock_detail: Optional[StockDetail] = None
    status: bool = True
    variants: list[ProductVariant] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    avg_rating: Optional[float] = None

    @property
    def price(self) -> Decimal:
        """Derived from price_entries. No price_entries means no price was
        ever generated for this product — returns 0 rather than raising, on
        the assumption that's a recoverable/displayable state (e.g. a
        not-yet-priced draft product), not a corrupted one. Reconsider this
        if an empty price_entries should instead signal a generator bug."""
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
