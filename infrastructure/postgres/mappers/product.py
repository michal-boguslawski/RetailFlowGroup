from domain.models import AlphaProduct
from infrastructure.postgres.models import AlphaProductORM


def orm_to_model(orm: AlphaProductORM) -> AlphaProduct:
    mapped_product = AlphaProduct(
        id=orm.product_id,
        name=orm.name,
        _price=orm.unit_price,
        category_path=orm.category_path,
    )
    # print(f"Mapped product {mapped_product}")
    return mapped_product 


def model_to_row(record: AlphaProduct) -> dict:
    return {
        "product_id": record.id,
        "category_path": record.category_path,
        "name": record.name,
        "unit_price": record.price,
    }
