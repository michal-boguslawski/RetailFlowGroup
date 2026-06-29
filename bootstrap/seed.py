import argparse
from pathlib import Path

from bootstrap.products import ProductSeeder
from config.loader import load_config
from domain.enums import StoreId
from config.models import StoreConfig
from generator.core.id_generator import IdGenerator
from infrastructure.mongo.factory import build_beta_db_service
from infrastructure.postgres.factory import build_alpha_db_service
from ingestion.loaders.alpha_product_loader import AlphaProductSeedLoader
from ingestion.loaders.beta_product_loader import BetaProductSeedLoader


PRODUCT_REGISTRY = {
    StoreId.ALPHA: (AlphaProductSeedLoader, build_alpha_db_service),
    StoreId.BETA: (BetaProductSeedLoader, build_beta_db_service),
}


def build_product_seeder(config: StoreConfig):
    """
    Build a product seeder for the given store.
    """
    path = Path(config.state_path) if config.state_path else None
    id_generator = IdGenerator(config.store_id, config.ids, path)

    loader_class, build_db_service = PRODUCT_REGISTRY[config.store_id]

    loader = loader_class(id_generator)
    db_service = build_db_service()

    return ProductSeeder(loader, db_service)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Seed products into store database"
    )

    parser.add_argument(
        "--store",
        required=True,
        choices=["alpha", "beta"],
        help="Target store"
    )

    parser.add_argument(
        "--csv",
        required=True,
        type=Path,
        help="Path to product CSV file"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.csv.exists():
        raise FileNotFoundError(
            f"CSV file not found: {args.csv}"
        )

    config = load_config(args.store)

    seeder = build_product_seeder(config)
    seeder.seed(args.csv)


if __name__ == "__main__":
    main()
