from functools import partial

from infrastructure.mongo.repositories.base import BaseRepository


UserProfileRepository = partial(BaseRepository, collection_name="user_profiles")
