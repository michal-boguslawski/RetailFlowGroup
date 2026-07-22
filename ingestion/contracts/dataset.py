from dataclasses import dataclass

@dataclass(frozen=True)
class DatasetContract:
    system: str
    entity: str
