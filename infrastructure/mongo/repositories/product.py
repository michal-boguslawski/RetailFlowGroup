from pymongo.database import Database

from domain.enums import Currency
from domain.models.product import BetaProduct
from infrastructure.mongo.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db, "products")

    def find_by_id(self, id_: str, *args, **kwargs) -> BetaProduct | None:
        doc = super().find_by_id(id_, *args, **kwargs)
        if doc is None:
            return None
        product = BetaProduct.from_document(doc)
        return product

    def find_random(self, currency: Currency | None = None, *args, **kwargs) -> BetaProduct | None:
        if currency:
            cursor = self.collection.aggregate([
                {
                    "$match": {
                        "$or": [
                            {
                                "prices.currency": currency.value
                            },
                            {
                                "price": {
                                    "$regex": currency.value,
                                    "$options": "i"
                                }
                            }
                        ]
                    }
                },
                {
                    "$sample": {
                        "size": 1
                    }
                }
            ])
        else:
            cursor = self.collection.aggregate([
                {
                    "$sample": {
                        "size": 1
                    }
                }
            ])
        result = cursor.to_list(length=1)
        if result:
            product = BetaProduct.from_document(result[0])
            return product
        return None
