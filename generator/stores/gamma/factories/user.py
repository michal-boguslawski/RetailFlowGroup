from domain.models.user import User
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory


class GammaUserFactory(BaseFactory[User]):
    def __init__(
        self,
        id_generator: IdGenerator,
    ):
        self.id_generator = id_generator

    def make_one(self, *args, **kwargs) -> User:
        return User(
            id=self.id_generator.make_id("user_id"),
            gdpr_consent=None
        )
