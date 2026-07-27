from dataclasses import dataclass

from domain.enums import OffsetWriter


@dataclass(frozen=True)
class KafkaOffsetRecord:
    topic: str
    partition: int
    offset: int
    writer: OffsetWriter
