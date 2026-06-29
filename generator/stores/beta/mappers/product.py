from dataclasses import asdict
from datetime import datetime
from domain.models import BetaProduct


def model_to_document(product: BetaProduct) -> dict:
    legacy = product.legacy_shape
    if legacy:
        return {
            "_id": product.id,
            "categoryPath": product.category,
            "prices": ",".join([f"{p.amount} {p.currency}" for p in product.price_entries]),
            "stock": product.stock_detail.total if product.stock_detail else None,
            "active": int(product.status),
            "tags": product.tags,
            "avgRating": product.avg_rating,
            "images": product.images,
            "updatedAt": datetime.now().isoformat(),
        }
    return {
        "_id": product.id,
        "categoryPath": product.category_path,
        "prices": [asdict(p) for p in product.price_entries],
        "stock": asdict(product.stock_detail) if product.stock_detail else None,
        "status": "active" if product.status else "inactive",
        "variants": [asdict(v) for v in product.variants],
        "tags": product.tags,
        "avgRating": product.avg_rating,
        "images": product.images,
        "updatedAt": datetime.now().isoformat(),
    }
