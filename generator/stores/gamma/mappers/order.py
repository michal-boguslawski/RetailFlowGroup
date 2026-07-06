from typing import Any

from domain.models import GammaOrder, Formatter


def model_to_dict(order: GammaOrder, formatter: Formatter) -> dict[str, Any]:
    return {
        formatter.column_naming_variants.order_id: order.id,
        formatter.column_naming_variants.user_id: order.user.id if order.user else None,
        formatter.column_naming_variants.order_date: 
            formatter.order_date_formattter_fn(order.order_date),
        formatter.column_naming_variants.total_amount:
            formatter.amount_formatter_fn(order),
        formatter.column_naming_variants.status: order.status.value,
        formatter.column_naming_variants.product_ids:
            "|".join(p.id for p in order.products),
        formatter.column_naming_variants.discount_code:
            order.promotion.promo_code if order.promotion else None,
        formatter.column_naming_variants.city: order.city,
    }
