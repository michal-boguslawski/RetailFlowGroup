from datetime import date

from domain.models.order_return import OrderReturn


class OrderReturnCatalog:
    def __init__(self):
        self._order_returns: list[OrderReturn] = []

    def upsert(self, order_return: OrderReturn):
        self._order_returns.append(order_return)

    def bulk_upsert(self, order_returns: list[OrderReturn]):
        self._order_returns.extend(order_returns)

    def find_by_id(self, id_: str) -> OrderReturn | None:
        for o in self._order_returns:
            if o.id == id_:
                return o
        return None

    def find_by_date(self, date_: date) -> list[OrderReturn]:
        return [o for o in self._order_returns if o.return_ts.date() == date_]
