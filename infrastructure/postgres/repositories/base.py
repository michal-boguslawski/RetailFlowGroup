from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.dialects.postgresql import Insert

from infrastructure.postgres.decorators import with_session


ModelT = TypeVar("ModelT")
OrmT = TypeVar("OrmT", bound=DeclarativeBase)


class BaseRepository(ABC, Generic[ModelT, OrmT]):
    def __init__(
        self,
        session_factory: sessionmaker,
    ):
        self._factory = session_factory
    
    def find_by_id(self, id_: str, *args, **kwargs) -> Optional[ModelT]:
        orm = self._find_by_id_orm(id_)
        if not orm:
            return None
        return self._orm_to_model_mapper(orm)

    @staticmethod
    @abstractmethod
    def _orm_to_model_mapper(orm: OrmT) -> ModelT: ...

    # @with_session
    def upsert(self, record: ModelT) -> None:
        self.bulk_upsert(records=[record])
        # session.execute(self._upsert_stmt([record]))

    @with_session
    def bulk_upsert(self, session: Session, records: list[ModelT]) -> None:
        if not records:
            return
        session.execute(self._upsert_stmt(records))

    @abstractmethod
    def _upsert_stmt(self, records: list[ModelT]) -> Insert:
        pass

    @abstractmethod
    def _find_by_id_orm(self, id_: str, *args, **kwargs) -> Optional[OrmT]:
        pass

    @abstractmethod
    def find_random(self, *args, **kwargs) -> Optional[ModelT]:
        pass
