from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import Insert, insert
from typing import Optional

from domain.models import User
from infrastructure.postgres.models import AlphaUserORM
from infrastructure.postgres.decorators import with_session
from infrastructure.postgres.mappers.user import orm_to_model, model_to_row
from infrastructure.postgres.repositories.base import BaseRepository


class AlphaUserRepository(BaseRepository[User, AlphaUserORM]):

    @with_session
    def _find_by_id_orm(self, session: Session, id_: str) -> AlphaUserORM | None:
        user_orm = session.get(AlphaUserORM, id_)
        return user_orm

    def _upsert_stmt(self, records: list[User]) -> Insert:
        rows = [model_to_row(u) for u in records]

        insert_stmt = insert(AlphaUserORM).values(rows)

        stmt = insert_stmt.on_conflict_do_update(
            index_elements=["user_id"],
            set_={
                "email": insert_stmt.excluded.email,
                "loyalty_tier": insert_stmt.excluded.loyalty_tier,
            },
        )
        return stmt

    @staticmethod
    def _orm_to_model_mapper(orm: AlphaUserORM) -> User:
        return orm_to_model(orm)

    @with_session
    def find_random(self, session: Session) -> Optional[User]:
        select_stmt = select(AlphaUserORM).order_by(func.random()).limit(1)
        orm = session.execute(select_stmt).scalar_one_or_none()
        if orm is None:
            return
        return self._orm_to_model_mapper(orm)
