from generator.stores.gamma.catalogs.order import OrderCatalog
from generator.stores.gamma.catalogs.order_return import OrderReturnCatalog
from generator.stores.gamma.catalogs.user import UserCatalog
from generator.stores.gamma.catalogs.product import ProductCatalog
from generator.stores.gamma.catalogs.promotion import PromotionCatalog
from infrastructure.core.db_service import DBService


def build_gamma_db_service() -> DBService:
    repos = {
        "orders": OrderCatalog(),
        "order_returns": OrderReturnCatalog(),
        "users": UserCatalog(),
        "products": ProductCatalog("data/seed/gamma_products.csv"),
        "promotions": PromotionCatalog(),
    }
    return DBService(repos)
