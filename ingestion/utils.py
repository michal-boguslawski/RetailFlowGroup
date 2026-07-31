import argparse
from datetime import datetime, date, time
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


def parse_date_since(value: str | None) -> datetime | None:
    """Parse --date_since accepting either 'YYYY-MM-DD' or full ISO datetime."""
    if value is None:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass

    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date_since '{value}': expected 'YYYY-MM-DD' or ISO datetime "
            f"(e.g. '2026-07-31T14:30:00')"
        )
