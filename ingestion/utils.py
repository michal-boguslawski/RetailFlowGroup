import json
from typing import Sequence

from domain.models.metadata import KafkaOffsetRecord


def parse_offsets(offsets: Sequence[KafkaOffsetRecord] | str, topic: str) -> str:
    if isinstance(offsets, str):
        return offsets

    _offsets: dict[str, int] = {
        str(r.partition): r.offset
        for r in offsets
    }
    return json.dumps({topic: _offsets})
