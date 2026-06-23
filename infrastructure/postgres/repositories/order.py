from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import Insert, insert
from typing import Optional

from domain.models import Order
from infrastructure.postgres.models import AlphaOrderORM, AlphaOrderItemORM
from infrastructure.postgres.decorators import with_session
from infrastructure.postgres.mappers.order import (
    order_orm_to_model,
    order_model_to_row
)
from infrastructure.postgres.repositories.base import BaseRepository


class AlphaOrderRepository(BaseRepository[Order, AlphaOrderORM]):

    @with_session
    def _find_by_id_orm(self, session: Session, id_: str) -> Optional[AlphaOrderORM]:
        user_orm = session.get(AlphaOrderORM, id_)
        return user_orm

    @staticmethod
    def _orm_to_model_mapper(orm: AlphaOrderORM) -> Order:
        return order_orm_to_model(orm)

    def upsert(self, record: Order) -> None:
        self.bulk_upsert(records=[record])

    @with_session
    def bulk_upsert(self, session: Session, records: list[Order]) -> None:
        order_rows = [order_model_to_row(record) for record in records]

        item_rows = []
        for order_row in order_rows:
            item_rows.extend(order_row.pop("items"))

        session.execute(
            self._upsert_order_stmt(order_rows)
        )

        session.execute(
            self._upsert_order_item_stmt(item_rows)
        )

    @staticmethod
    def _upsert_order_stmt(order_rows: list[dict]) -> Insert:
        stmt = insert(AlphaOrderORM).values(order_rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["order_id"],
            set_=dict(stmt.excluded),
        )
        return stmt

    @staticmethod
    def _upsert_order_item_stmt(item_rows: list[dict]) -> Insert:
        stmt = insert(AlphaOrderItemORM).values(item_rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=["order_item_id"])
        return stmt

    def _upsert_stmt(self, records: list[Order]) -> Insert:  # pyright: ignore[reportReturnType]
        pass

    @with_session
    def find_random(self, session: Session) -> Optional[Order]:
        select_stmt = select(AlphaOrderORM).order_by(func.random()).limit(1)
        orm = session.execute(select_stmt).scalar_one_or_none()
        if orm is None:
            return
        return self._orm_to_model_mapper(orm)
