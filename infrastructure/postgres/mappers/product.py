from domain.models import Product
from infrastructure.postgres.models import AlphaProductORM


def orm_to_model(orm: AlphaProductORM) -> Product:
    mapped_product = Product(
        id=orm.product_id,
        name=orm.name,
        price=orm.unit_price,
        category_path=orm.category_path,
    )
    # print(f"Mapped product {mapped_product}")
    return mapped_product 


def model_to_row(record: Product) -> dict:
    return {
        "product_id": record.id,
        "category_path": record.category_path,
        "name": record.name,
        "unit_price": record.price,
    }
