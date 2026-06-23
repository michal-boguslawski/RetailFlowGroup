from pathlib import Path

from bootstrap.products import ProductSeeder
from config.loader import load_config
from config.models import StoreConfig
from generator.core.id_generator import IdGenerator
from infrastructure.postgres.factory import build_alpha_db_service
from ingestion.loaders.product_loader import ProductSeedLoader


def build_product_seeder(config: StoreConfig):
    """
    Build a product seeder for the given store.
    """
    path = Path(config.state_path) if config.state_path else None
    id_generator = IdGenerator(config.store_id, config.ids, path)
    loader = ProductSeedLoader(id_generator)
    db_service = build_alpha_db_service()
    product_seeder = ProductSeeder(loader, db_service)
    return product_seeder


if __name__ == "__main__":
    config = load_config("alpha")
    seeder = build_product_seeder(config)
    seeder.seed("data/seed/alpha_products.csv")
