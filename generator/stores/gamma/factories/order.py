from datetime import date
from faker import Faker

from domain.enums import OrderStatus, Currency
from domain.models.order import GammaOrder
from domain.models.product import GammaProduct, Product
from domain.models.promotion import Promotion
from domain.models.user import User
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory
from infrastructure.core.db_service import DBService


class GammaOrderFactory(BaseFactory[GammaOrder]):
    def __init__(
        self,
        id_generator: IdGenerator,
        db_service: DBService,
        fake: Faker | None = None,
    ):
        self.fake = fake or make_faker()
        self.id_generator = id_generator
        self.db_service = db_service

    def make_one(self, date_: date) -> GammaOrder:
        user = self.db_service.get_random("users")
        if not isinstance(user, User):
            raise TypeError(f"user is not User type, but {type(user)}")

        currency = self.fake.random_element([Currency.PLN, Currency.EUR])

        n_products = self.fake.random_int(min=1, max=10)
        products: list[Product] = []
        for _ in range(n_products):
            product = self.db_service.get_random("products", date_=date_, currency=currency)
            if not isinstance(product, GammaProduct):
                raise TypeError(f"product is not GammaProduct type, but {type(product)}")
            products.append(product)

        promotion = self.db_service.get_random("promotions", date_=date_, amount=sum(p.price for p in products))
        if promotion is not None and not isinstance(promotion, Promotion):
            raise TypeError(f"promotion is not Promotion type, but {type(promotion)}")

        return GammaOrder(
            id = self.id_generator.make_id("order_id"),
            user = user,
            order_date = date_,
            status = self.fake.random_element(list(OrderStatus)),
            products = products,
            promotion = promotion,
            city = self.fake.city(),
            currency = currency,
        )
