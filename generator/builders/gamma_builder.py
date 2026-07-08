from pathlib import Path

from config.models import StoreConfig
from config.loader import load_lake_config
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.factory import StoreFactory
from generator.stores.gamma.filename_config import FileNamingConfig
from generator.stores.gamma.factory import build_gamma_db_service
from generator.stores.gamma.factories.order import GammaOrderFactory
from generator.stores.gamma.factories.user import GammaUserFactory
from generator.stores.gamma.factories.order_return import GammaOrderReturnFactory
from generator.stores.gamma.factories.promotion import GammaPromotionFactory
from generator.stores.gamma.factories.formatter import GammaFormatterFactory
from generator.stores.gamma.generator_handler import GammaEventHandler
from generator.stores.gamma.router import GammaRouter
from infrastructure.minio.factory import build_minio_service
from sinks.file import FileSink
from sinks.postgres import PostgresSink


class GammaBuilder:
    def __init__(self):
        self.db_service = build_gamma_db_service()
        self.lake_config = load_lake_config()

    def _build_file_sink(self, config: StoreConfig) -> FileSink:
        file_service = build_minio_service()
        filename_config = FileNamingConfig()
        return FileSink(file_service, filename_config, self.lake_config.landing.bucket)

    def _build_db_sink(self, config: StoreConfig) -> PostgresSink:
        return PostgresSink(self.db_service)

    def build_router(self, config: StoreConfig) -> GammaRouter:
        # --- sinks ---
        file_sink = self._build_file_sink(config)
        db_sink = self._build_db_sink(config)

        # --- router ---
        return GammaRouter(file_sink, db_sink)

    def build_factory(self, config: StoreConfig) -> StoreFactory:
        faker = make_faker(locale="en_US")
        state_path = Path(config.state_path) if config.state_path else None
        ids = IdGenerator(config.store_id, config.ids, state_path=state_path)
        
        gamma_factories = {
            "users": GammaUserFactory(ids),
            "orders": GammaOrderFactory(ids, self.db_service, faker),
            "order_returns": GammaOrderReturnFactory(ids, self.db_service, faker),
            "promotions": GammaPromotionFactory(faker),
            "formatters": GammaFormatterFactory(faker),
        }
        return StoreFactory(gamma_factories)

    def build_handler(self, config: StoreConfig) -> GammaEventHandler:
        store_factory = self.build_factory(config)
        return GammaEventHandler(
            store_factory,
            self.db_service,
        )
