from decimal import Decimal
from typing import Any, Hashable

from domain.models import GammaProduct, Formatter


def row_to_model(row: dict[Hashable, Any]) -> GammaProduct:
    return GammaProduct(
        id = str(row["id"]),
        name = row["name"],
        category = row["category"],
        _price = Decimal(row["price"]),
        stock_count = row["stock_count"],
        ean_barcode = row["ean_barcode"],
        active = row["active"],
        created_date = row["created_date"],
    )


def model_to_dict(product: GammaProduct, formatter: Formatter) -> dict[str, Any]:
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
        "stock_count": product.stock_count,
        "ean_barcode": product.ean_barcode,
        "active": product.active,
        "created_date": product.created_date.strftime("%Y%M%d"),
    }

