# ingestion/loaders/product_loader.py
import pandas as pd

from domain.models import Product
from generator.core.id_generator import IdGenerator


class ProductSeedLoader:
    def __init__(self, id_generator: IdGenerator):
        self._id_generator = id_generator

    def _parse_product(self, row: dict) -> Product:
        stock_count = row.get("stock_count")
        active = row.get("active")
        tax_pc = row.get("tax_pc")
        avg_rating = row.get("avg_rating")

        return Product(
            id=self._id_generator.make_id("product_id"),
            name=row["name"],
            price=float(row["price"]),
            category_path=row["category_path"],
            stock_count=int(stock_count) if stock_count else None,
            ean_barcode=row.get("ean_barcode"),
            active=bool(active) if active else None,
            tax_pc=float(tax_pc) if tax_pc else None,
            avg_rating=float(avg_rating) if avg_rating else avg_rating,
            currency=row.get("currency"),
        )

    def load(self, path: str) -> list[Product]:
        df = pd.read_csv(path)
        return [self._parse_product(row.to_dict()) for _, row in df.iterrows()]
