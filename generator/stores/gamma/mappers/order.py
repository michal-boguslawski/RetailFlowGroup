from typing import Any

from domain.models.order import GammaOrder


def model_to_row(order: GammaOrder) -> dict[str, Any]:
    return {
        "order_id": order.id,
        "user_id": order.user.id,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "status": order.status.value,
        "product_ids": "|".join(p.id for p in order.products),
        "promotion": order.promotion.promo_code,
        "city": order.city,
    }
