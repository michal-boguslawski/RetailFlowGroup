from domain.enums import Currency
from domain.models import Order, OrderLineItem
from infrastructure.postgres.models import AlphaOrderORM, AlphaOrderItemORM
from infrastructure.postgres.mappers.product import orm_to_model as product_orm_to_model
from infrastructure.postgres.mappers.user import orm_to_model as user_orm_to_model


def order_item_orm_to_model(orm: AlphaOrderItemORM) -> OrderLineItem:

    product = product_orm_to_model(orm.product)
    if not product:
        raise ValueError("Missing Product info")

    return OrderLineItem(
        id=orm.order_item_id,
        product=product,
        quantity=orm.quantity,
        discount_pct=orm.discount_pct,
    )


def order_orm_to_model(orm: AlphaOrderORM) -> Order:
    items = [
        order_item_orm_to_model(item)
        for item in orm.items
    ]

    return Order(
        id=orm.order_id,
        user=user_orm_to_model(orm.user),
        currency=Currency(orm.currency),
        guest_email=orm.guest_email,
        items=items,
        notes=orm.notes,
    )


def order_item_model_to_row(order_item: OrderLineItem, order_id: str) -> dict:
    return {
        "quantity": order_item.quantity,
        "discount_pct": order_item.discount_pct,
        "order_id": order_id,
        "product_id": order_item.product.id,
    }


def order_model_to_row(record: Order) -> dict:
    order_items = [
        order_item_model_to_row(item, record.id)
        for item in record.items
    ]
    return {
        "order_id": record.id,
        "user_id": record.user.id if record.user else None,
        "currency": record.currency.value,
        "guest_email": record.guest_email,
        "total_price": record.total_amount,
        "tax_price": record.tax_amount,
        "notes": record.notes,
        # "status": "completed",
        "items": order_items,
    }
