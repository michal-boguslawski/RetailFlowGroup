from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.orm import Session
from typing import Optional, Sequence

from domain.enums import OffsetWriter
from domain.models.metadata import KafkaOffsetRecord
from infrastructure.postgres.decorators import with_session
from infrastructure.postgres.models import KafkaOffset
from infrastructure.postgres.repositories.base import BaseRepository


class KafkaOffsetRepository(BaseRepository[KafkaOffsetRecord, KafkaOffset]):

    @staticmethod
    def _orm_to_model_mapper(orm: KafkaOffset) -> KafkaOffsetRecord:
        return KafkaOffsetRecord(
            topic=orm.topic,
            partition=orm.partition,
            offset=orm.offset,
            writer=OffsetWriter(orm.last_writer),
        )

    @with_session
    def _find_all_orm(self, session: Session, topic: str) -> list[KafkaOffset]:
        return (
            session.query(KafkaOffset)
            .filter(KafkaOffset.topic == topic)
            .all()
        )

    def _upsert_stmt(self, records: list[KafkaOffsetRecord]) -> Insert:
        values = [
            {"topic": r.topic, "partition": r.partition, "offset": r.offset, "last_writer": r.writer.value}
            for r in records
        ]
        stmt = insert(KafkaOffset).values(values)
        return stmt.on_conflict_do_update(
            index_elements=["topic", "partition"],
            set_={"offset": stmt.excluded.offset, "last_writer": stmt.excluded.last_writer},
        )

    def _find_by_id_orm(self, id_: str, *args, **kwargs) -> Optional[KafkaOffset]:
        raise NotImplementedError("KafkaOffsetRepository has no single-id lookup")

    def find_random(self, *args, **kwargs) -> Optional[KafkaOffsetRecord]:
        raise NotImplementedError("KafkaOffsetRepository does not support find_random")

    def find_by_date(self, *args, **kwargs) -> Sequence[KafkaOffsetRecord]:
        raise NotImplementedError("KafkaOffsetRepository does not support find_by_date")
