from pymongo.database import Database

from domain.models.user import BetaUser
from infrastructure.mongo.repositories.base import BaseRepository
from infrastructure.mongo.mappers.profile import document_to_model


class UserProfileRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db, "user_profiles")

    def find_by_id(self, id_: str, *args, **kwargs) -> BetaUser | None:
        doc = super().find_by_id(id_, *args, **kwargs)
        if doc is None:
            return None
        product = document_to_model(doc)
        return product

    def find_random(self, *args, **kwargs) -> BetaUser:
        doc = super().find_random(*args, **kwargs)
        if not isinstance(doc, dict):
            raise TypeError("Expected a dictionary, got {}".format(type(doc)))
        return document_to_model(doc)
