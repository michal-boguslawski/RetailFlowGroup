from functools import partial

from infrastructure.mongo.repositories.base import BaseRepository


ProductRepository = partial(BaseRepository, collection_name="products")
