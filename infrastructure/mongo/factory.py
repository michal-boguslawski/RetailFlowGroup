# infrastructure/mongo/factory.py
from domain.enums import Currency
from infrastructure.core.db_service import DBService
from infrastructure.config.settings import MongoDBSettings
from infrastructure.mongo.client import MongoClient
from infrastructure.mongo.repositories.product import ProductRepository
from infrastructure.mongo.repositories.profile import UserProfileRepository


def build_beta_db_service() -> DBService:
    settings = MongoDBSettings()
    mongo_client = MongoClient(settings)
    database = mongo_client.get_database()

    repos = {
        "users": UserProfileRepository(database),
        "products": ProductRepository(database),
    }

    return DBService(repos)


if __name__ == "__main__":
    db_service = build_beta_db_service()
    print(db_service.get_random("products", currency=Currency.PLN))
