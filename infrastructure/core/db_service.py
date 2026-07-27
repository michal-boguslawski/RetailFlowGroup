# infrastructure/core/db_service.py
from datetime import date
from typing import Protocol, TypeVar, runtime_checkable, Sequence, Optional, Mapping

from domain.types import GeneratedRecord

T = TypeVar("T")


@runtime_checkable
class Repository(Protocol[T]):
    def upsert(self, record: T) -> None: ...
    def bulk_upsert(self, records: Sequence[T]) -> None: ...
    def find_by_id(self, id_: str, *args, **kwargs) -> Optional[T]: ...
    def find_random(self, *args, **kwargs) -> Optional[T]: ...
    def find_by_date(
        self,
        date_: date | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        *args,
        **kwargs
    ) -> Sequence[T]: ...
    def find_all(self, *args, **kwargs) -> Sequence[T]: ...


class DBService:
    """
    Generic service composing multiple repositories under string keys.
    Database-specific logic (SQL statements, bulk_write semantics)
    lives entirely inside the repositories — this class only routes.
    """

    def __init__(self, repositories: Mapping[str, Repository]):
        self._repos = repositories

    def save(self, entity_name: str, record: object) -> None:
        repo = self._get_repo(entity_name)
        repo.upsert(record)

    def bulk_save(self, entity_name: str, records: Sequence[T]) -> None:
        if not records:
            return
        repo = self._get_repo(entity_name)
        repo.bulk_upsert(records)

    def get(self, entity_name: str, id_: str, *args, **kwargs) -> GeneratedRecord | None:
        repo = self._get_repo(entity_name)
        return repo.find_by_id(id_, *args, **kwargs)

    def _get_repo(self, entity_name: str) -> Repository:
        try:
            return self._repos[entity_name]
        except KeyError:
            raise ValueError(
                f"No repository registered for entity '{entity_name}'. "
                f"Available: {list(self._repos.keys())}"
            )

    def get_random(self, entity_name: str, *args, **kwargs) -> GeneratedRecord | None:
        repo = self._get_repo(entity_name)
        return repo.find_random(*args, **kwargs)

    def get_at_date(
        self,
        entity_name: str,
        date_: date | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        *args,
        **kwargs
    ) -> Sequence[GeneratedRecord]:
        repo = self._get_repo(entity_name)
        return repo.find_by_date(date_=date_, from_date=from_date, to_date=to_date, *args, **kwargs)

    def get_all(
        self, 
        entity_name: str,
        *args,
        **kwargs
    ) -> Sequence[GeneratedRecord] | None:
        repo = self._get_repo(entity_name)
        return repo.find_all(*args, **kwargs)
