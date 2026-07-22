from dataclasses import dataclass

from ingestion.contracts.source import SourceContract
from ingestion.contracts.dataset import DatasetContract
from ingestion.contracts.target import TargetContract
from ingestion.contracts.job import JobContract

@dataclass(frozen=True)
class IngestionContract:
    name: str
    job: JobContract
    source: SourceContract
    dataset: DatasetContract
    target: TargetContract
