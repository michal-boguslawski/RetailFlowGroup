from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import Insert, insert
from typing import Optional

from domain.models import AlphaProduct
from infrastructure.postgres.models import AlphaProductORM
from infrastructure.postgres.decorators import with_session
from infrastructure.postgres.mappers.product import orm_to_model, model_to_row
from infrastructure.postgres.repositories.base import BaseRepository


class AlphaProductRepository(BaseRepository[AlphaProduct, AlphaProductORM]):

    @with_session
    def _find_by_id_orm(self, session: Session, id_: str) -> AlphaProductORM | None:
        product_orm = session.get(AlphaProductORM, id_)
        return product_orm

    def _upsert_stmt(self, records: list[AlphaProduct]) -> Insert:
        rows = [model_to_row(record) for record in records]
        stmt = insert(AlphaProductORM).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["product_id"],
            set_=dict(stmt.excluded),
        )
        return stmt

    @staticmethod
    def _orm_to_model_mapper(orm: AlphaProductORM) -> AlphaProduct:
        return orm_to_model(orm)

    @with_session
    def find_random(self, session: Session) -> Optional[AlphaProduct]:
        select_stmt = select(AlphaProductORM).order_by(func.random()).limit(1)
        orm = session.execute(select_stmt).scalar_one_or_none()
        # print(f"Found product orm {orm}")
        if orm is None:
            return
        return self._orm_to_model_mapper(orm)
    