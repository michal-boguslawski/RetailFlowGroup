# ingestion/loaders/product_loader.py
from decimal import Decimal
import pandas as pd

from domain.models import AlphaProduct
from ingestion.loaders.base_product_loader import BaseProductSeedLoader


class AlphaProductSeedLoader(BaseProductSeedLoader):

    def _parse_product(self, row: dict) -> AlphaProduct:
        tax_pc = row.get("tax_pc")

        return AlphaProduct(
            id=self._id_generator.make_id("product_id"),
            name=row["name"],
            _price=Decimal(row["price"]),
            category_path=row["category_path"],
            tax_pc=Decimal(tax_pc) if tax_pc else None,
            currency=row.get("currency"),
        )

    def load(self, path: str) -> list[AlphaProduct]:
        df = pd.read_csv(path)
        return [self._parse_product(row.to_dict()) for _, row in df.iterrows()]
