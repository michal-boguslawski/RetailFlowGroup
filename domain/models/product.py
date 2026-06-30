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
        price_entry = self.price_entries[0]
        return price_entry.amount * (1 + price_entry.vat_rate / 100)

    @property
    def category(self) -> str:
        """Legacy flat representation, derived from the canonical hierarchy.
        Used by the mapper when legacy_shape=True. Currently takes the leaf
        category; change to '/'.join(self.category_path) if your reference
        legacy shape used a joined path instead."""
        if not self.category_path:
            return ""
        return '/'.join(self.category_path)

    @classmethod
    def from_document(cls, doc: dict) -> "BetaProduct":
        """Dispatches to the correct parser based on document shape."""
        if "category" in doc:
            return cls._from_legacy_document(doc)
        return cls._from_modern_document(doc)

    @classmethod
    def _from_legacy_document(cls, doc: dict) -> "BetaProduct":
        return cls(
            id=doc["_id"],
            # name=doc["name"],
            name="",
            category_path=[doc["category"].split("/")],
            legacy_shape=True,
            price_entries=[PriceEntry(
                country="UNKNOWN",
                currency=doc["price"].split(" ")[-1],
                amount=Decimal(doc["price"].split(" ")[0]),
                vat_rate=Decimal("0"),
            )],
            stock_detail=StockDetail(
                total=doc["stock"],
                reserved=0,
                warehouses={},),
            status=bool(doc["status"]),
            tags=doc["tags"],
            images=doc["images"],
            avg_rating=doc["avg_rating"],
        )

    @classmethod
    def _from_modern_document(cls, doc: dict) -> "BetaProduct":
        # avg_rating: Optional[float] = None
        return cls(
            id=doc["_id"],
            # name=doc["name"],
            name="",
            category_path=doc.get("categoryPath", []),
            legacy_shape=False,
            price_entries=[
                PriceEntry(country=p["country"], currency=p["currency"],
                           amount=Decimal(str(p["amount"])), vat_rate=Decimal(str(p["vatRate"])))
                for p in doc.get("prices", [])
            ],
            stock_detail=StockDetail(**doc["stock"]) if doc.get("stock") else None,
            status=( doc["status"] == "active" ),
            variants=[ProductVariant(**v) for v in doc.get("variants", [])],
            tags=doc.get("tags", []),
            images=doc.get("images", []),
            avg_rating=doc.get("avgRating"),
        )
