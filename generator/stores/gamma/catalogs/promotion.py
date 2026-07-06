from datetime import date
from decimal import Decimal
import random

from domain.models.promotion import Promotion


class PromotionCatalog:
    def __init__(self):
        self._promotions: dict[str, Promotion] = {}

    def upsert(self, promotion: Promotion):
        if promotion.promo_code in self._promotions:
            return
        self._promotions[promotion.promo_code] = promotion

    def bulk_upsert(self, promotions: list[Promotion]):
        for p in promotions:
            self.upsert(p)

    def find_random(self, date_: date, amount: Decimal | None = None) -> Promotion | None:
        valid_promos = [
            p for p in self._promotions.values()
            if p.is_active(date_) and (amount is None or p.is_applicable(amount))
        ]

        if not valid_promos:
            return None

        promo = random.choice(valid_promos)
        return promo

    def find_by_id(self, id_: str) -> Promotion | None:
        return self._promotions.get(id_, None)

    def find_by_date(self, date_: date, *args, **kwargs) -> list[Promotion]:
        return [
            p for p in self._promotions.values()
            if p.valid_from == date_
        ]
        