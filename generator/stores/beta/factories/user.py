from faker import Faker
from typing import cast

from domain.enums import PrefferedLanguages
from domain.models import BetaUser, BetaProduct
from infrastructure.core.db_service import DBService
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory


class BetaUserFactory(BaseFactory[BetaUser]):
    def __init__(
        self,
        id_generator: IdGenerator,
        db_service: DBService,
        fake: Faker | None = None,
    ):
        self.fake = fake or make_faker()
        self.id_generator = id_generator
        self.db_service = db_service

    def _generate_size_preferences(self, n: int) -> dict[str, str]:
        size_preferences = {}
        for _ in range(n):
            product = cast(BetaProduct, self.db_service.get_random("products"))
            if product.variants:
                size_preferences[product.category_path[-1]] = self.fake.random_element(product.variants).size
        return size_preferences

    def _generate_wishlist(self, n: int) -> list[str]:
        wishlist = []
        for _ in range(n):
            product = cast(BetaProduct, self.db_service.get_random("products"))
            wishlist.append(product.id)
        return list(set(wishlist))

    def make_one(self) -> BetaUser:
        return BetaUser(
            id = self.id_generator.make_id("user_id"),
            email_hash=self.fake.hashed(self.fake.email()),
            phone_hash=self.fake.hashed(self.fake.phone_number()),
            preferred_language=self.fake.random_element(list(PrefferedLanguages)),
            size_preferences=self._generate_size_preferences(self.fake.random_int(0, 5)),
            wishlist=self._generate_wishlist(self.fake.random_int(0, 5)),
            loyalty_points=self.fake.random_int(0, 10_000),
            gdpr_consent = self.fake.boolean(),
        )
    