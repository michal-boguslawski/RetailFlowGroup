import json
import pandas as pd
from pathlib import Path

from config.loader import load_config
from domain.models.product import BetaProduct, PriceEntry, StockDetail, ProductVariant
from generator.stores.beta.mappers.product import model_to_document
from ingestion.loaders.base_product_loader import BaseProductSeedLoader


class BetaProductSeedLoader(BaseProductSeedLoader):

    def _parse_product(self, series: pd.Series) -> BetaProduct:
        legacy = bool(series["legacy"])
        return BetaProduct(
            id=self._id_generator.make_id("product_id_legacy") if legacy else self._id_generator.make_id("product_id"),
            name="",
            category_path=series["category_path"],
            status=bool(series["active"]),
            price_entries=[PriceEntry(**price_entry) for price_entry in series["prices"]],
            stock_detail=StockDetail(**series["stock"]) if series["stock"] else None,
            variants=[ProductVariant(**variant) for variant in series["variants"]],
            tags=series["tags"],
            images=series["images"],
            avg_rating=series["avg_rating"],
            legacy_shape=legacy,
        )

    def load(self, path: str) -> list[dict]:
        df = pd.read_csv(path)

        for col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, int) or isinstance(x, float) else json.loads(x))

        products = [self._parse_product(row) for _, row in df.iterrows()]
        documents = [model_to_document(p) for p in products]
        return documents
    