from decimal import Decimal

from domain.models.product import BetaProduct, PriceEntry, StockDetail, ProductVariant


def _from_legacy_document_to_model(doc: dict) -> BetaProduct:
    return BetaProduct(
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
        status=bool(doc["active"]),
        tags=doc.get("tags", []),
        images=doc["images"],
        avg_rating=doc.get("avgRating"),
    )

def _from_modern_document_to_model(doc: dict) -> BetaProduct:
    return BetaProduct(
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
        images=doc["images"],
        avg_rating=doc.get("avgRating"),
    )

def document_to_model(doc: dict) -> BetaProduct:
    """Dispatches to the correct parser based on document shape."""
    if "category" in doc:
        return _from_legacy_document_to_model(doc)
    return _from_modern_document_to_model(doc)
