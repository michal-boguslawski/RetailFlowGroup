from infrastructure.core.db_service import DBService
from ingestion.loaders.base_product_loader import BaseProductSeedLoader


class ProductSeeder:

    def __init__(
        self,
        loader: BaseProductSeedLoader, 
        db_service: DBService,
    ):
        self.loader = loader
        self.db_service = db_service

    def seed(self, path: str):
        products = self.loader.load(path)
        self.db_service.bulk_save("products", products)
