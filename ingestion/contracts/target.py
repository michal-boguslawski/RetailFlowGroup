from dataclasses import dataclass


@dataclass(frozen=True)
class TargetContract:
    layer: str
    format: str
    mode: str
    options: dict
