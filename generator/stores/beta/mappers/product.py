from dataclasses import asdict
from datetime import datetime
from domain.models import BetaProduct


def model_to_document(product: BetaProduct) -> dict:
    legacy = product.legacy_shape
    if legacy:
        price_entry = product.price_entries[0]
        return {
            "_id": product.id,
            "category": product.category,
            "price": f"{price_entry.amount} {price_entry.currency}",
            "stock": product.stock_detail.total if product.stock_detail else None,
            "active": int(product.status),
            "tags": product.tags,
            "avgRating": product.avg_rating,
            "images": product.images,
            "updatedAt": datetime.now().isoformat(),
        }

    price_entries = []
    for p in product.price_entries:
        d = asdict(p)
        d["vatRate"] = d.pop("vat_rate")
        price_entries.append(d)

    return {
        "_id": product.id,
        "categoryPath": product.category_path,
        "prices": price_entries,
        "stock": asdict(product.stock_detail) if product.stock_detail else None,
        "status": "active" if product.status else "inactive",
        "variants": [asdict(v) for v in product.variants],
        "tags": product.tags,
        "avgRating": product.avg_rating,
        "images": product.images,
        "updatedAt": datetime.now().isoformat(),
    }
