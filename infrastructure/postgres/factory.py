# infrastructure/postgres/factory.py
from infrastructure.core.db_service import DBService
from infrastructure.config.settings import PostgresSettings
from infrastructure.postgres.session import create_session_factory
from infrastructure.postgres.repositories.user import AlphaUserRepository
from infrastructure.postgres.repositories.order import AlphaOrderRepository
from infrastructure.postgres.repositories.product import AlphaProductRepository


def build_alpha_db_service() -> DBService:
    settings = PostgresSettings()
    session_factory = create_session_factory(settings)

    repos = {
        "users": AlphaUserRepository(session_factory),
        "orders": AlphaOrderRepository(session_factory),
        "products": AlphaProductRepository(session_factory),
    }

    return DBService(repos)
