from typing import Any, Hashable

from domain.models.product import GammaProduct


def row_to_model(row: dict[Hashable, Any]) -> GammaProduct:
    return GammaProduct(
        id = row["id"],
        name = row["name"],
        category = row["category"],
        _price = row["price"],
        stock_count = row["stock_count"],
        ean_barcode = row["ean_barcode"],
        active = row["active"],
        created_date = row["created_date"],
    )
    