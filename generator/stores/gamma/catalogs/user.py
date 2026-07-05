from datetime import date
import random

from domain.enums import OrderStatus
from domain.models.user import User


class UserCatalog:
    def __init__(self):
        self._users: list[User] = []

    def upsert(self, user: User):
        self._users.append(user)

    def bulk_upsert(self, users: list[User]):
        self._users.extend(users)

    def find_by_id(self, id_: str) -> User | None:
        for o in self._users:
            if o.id == id_:
                return o
        return None

    def find_random(self) -> User | None:
        if not self._users:
            return None
        return random.choice(self._users)
