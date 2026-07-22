from dataclasses import dataclass


@dataclass(frozen=True)
class SourceContract:
    type: str
    options: dict
