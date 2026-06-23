# infrastructure/core/db_service.py

from typing import Protocol, TypeVar, runtime_checkable, Sequence, Optional

from domain.types import GeneratedRecord

T = TypeVar("T")


@runtime_checkable
class Repository(Protocol[T]):
    def upsert(self, record: T) -> None: ...
    def bulk_upsert(self, records: Sequence[T]) -> None: ...
    def find_by_id(self, id_: str) -> Optional[T]: ...
    def find_random(self) -> Optional[T]: ...


class DBService:
    """
    Generic service composing multiple repositories under string keys.
    Database-specific logic (SQL statements, bulk_write semantics)
    lives entirely inside the repositories — this class only routes.
    """

    def __init__(self, repositories: dict[str, Repository]):
        self._repos = repositories

    def save(self, entity_name: str, record: object) -> None:
        repo = self._get_repo(entity_name)
        repo.upsert(record)

    def bulk_save(self, entity_name: str, records: Sequence[T]) -> None:
        if not records:
            return
        repo = self._get_repo(entity_name)
        repo.bulk_upsert(records)

    def get(self, entity_name: str, id_: str) -> GeneratedRecord | None:
        repo = self._get_repo(entity_name)
        return repo.find_by_id(id_)

    def _get_repo(self, entity_name: str) -> Repository:
        try:
            return self._repos[entity_name]
        except KeyError:
            raise ValueError(
                f"No repository registered for entity '{entity_name}'. "
                f"Available: {list(self._repos.keys())}"
            )

    def get_random(self, entity_name: str) -> GeneratedRecord | None:
        repo = self._get_repo(entity_name)
        return repo.find_random()
