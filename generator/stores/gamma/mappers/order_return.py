from typing import Any

from domain.models import OrderReturn, Formatter


def model_to_dict(order_return: OrderReturn, formatter: Formatter) -> dict[str, Any]:
    dict_ = {
        "return_id": order_return.return_id,
        "order_id": order_return.order.id,
        "return_ts": order_return.return_ts.isoformat(),
        "customer_id": order_return.user.id if order_return.user else None,
        "reason_code": order_return.reason_code.value,
        "condition": order_return.condition.value,
        "items": (
            order_return.items[0].id if len(order_return.items) == 1
            else [i.id for i in order_return.items]
        ),
    }
    if order_return.refund_amount:
        dict_["refund_amount"] = order_return.refund_amount
    
    return dict_
