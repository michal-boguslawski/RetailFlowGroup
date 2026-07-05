from datetime import date
import random

from domain.enums import OrderStatus
from domain.models.order import GammaOrder


class OrderCatalog:
    def __init__(self):
        self._orders: list[GammaOrder] = []

    def upsert(self, order: GammaOrder):
        self._orders.append(order)

    def bulk_upsert(self, orders: list[GammaOrder]):
        self._orders.extend(orders)

    def find_by_date(self, date_ = date) -> list[GammaOrder]:
        return [o for o in self._orders if o.order_date == date_]

    def find_by_id(self, id_: str) -> GammaOrder | None:
        for o in self._orders:
            if o.id == id_:
                return o
        return None

    def find_random(self, order_status: OrderStatus | None = None) -> GammaOrder | None:
        if not self._orders:
            return None

        appicable_orders = self._orders
        if order_status:
            appicable_orders = [
                o for o in appicable_orders if o.status == order_status
            ]

        return random.choice(appicable_orders)
