from datetime import date
from decimal import Decimal
import pandas as pd

from domain.enums import Currency
from domain.models.product import GammaProduct
from generator.stores.gamma.mappers.product import row_to_model


CONVERSION_RATES = {
    Currency.PLN: Decimal(1),
    Currency.GBP: Decimal(0.20),
    Currency.EUR: Decimal(0.23),
}


class ProductCatalog:

    def __init__(self, path: str):
        self._products_df = self._load(path)

    def _load(self, path):
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".json"):
            df = pd.read_json(path)
        else:
            raise ValueError("Unsupported format")

        df["created_date"] = pd.to_datetime(df["created_date"])

        return df

    @staticmethod
    def _process_dict_to_model(product: dict, currency: Currency | None = None) -> GammaProduct:
        product_model = row_to_model(product)

        if currency:
            product_model.net_price = product_model.net_price * CONVERSION_RATES[currency]
        return product_model

    def find_random(self, date_: date, currency: Currency) -> GammaProduct:
        candidates = self._products_df[
            self._products_df["created_date"] <= pd.Timestamp(date_)
        ].dropna()

        if candidates.empty:
            raise ValueError(f"No products available on {date_}")

        product = candidates.sample(n=1).iloc[0].to_dict()
        return self._process_dict_to_model(product, currency)

    def find_by_date(self, date_: date | None = None, from_date: date | None = None, to_date: date | None = None) -> list[GammaProduct] | None:
        candidates = self._products_df
        if date_:
            candidates = candidates[candidates["created_date"] == pd.Timestamp(date_)].dropna()

        if from_date:
            candidates = candidates[candidates["created_date"] >= pd.Timestamp(from_date)].dropna()

        if to_date:
                candidates = candidates[candidates["created_date"] <= pd.Timestamp(to_date)].dropna()

        if candidates.empty:
            return

        return [
            self._process_dict_to_model(product)
            for product in candidates.to_dict("records")
        ]

    def find_by_id(self, id_: str, currency: Currency):
        product = (
            self._products_df[self._products_df["id"] == id_]
            .iloc[0]
            .to_dict()
        )
        return self._process_dict_to_model(product, currency)
