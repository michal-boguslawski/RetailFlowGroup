from typing import Any

from domain.models import Promotion, Formatter


def model_to_dict(promotion: Promotion, formatter: Formatter) -> dict[str, Any]:
    return {
        formatter.column_naming_variants.promo_code: promotion.promo_code,
        formatter.column_naming_variants.discount_value: 
            formatter.discount_value_formatter_fn(promotion.discount_value),
        formatter.column_naming_variants.valid_from: 
            formatter.valid_formatter_fn(promotion.valid_from),
        formatter.column_naming_variants.valid_to: 
            formatter.valid_formatter_fn(promotion.valid_to) if promotion.valid_to else None,
        formatter.column_naming_variants.min_order_value: 
            formatter.min_order_value_formatter_fn(promotion),
        formatter.column_naming_variants.discount_type: promotion.discount_type.value,
    }