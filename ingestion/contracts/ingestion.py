from pydantic import BaseModel

from ingestion.contracts.source import SourceContract
from ingestion.contracts.dataset import DatasetContract
from ingestion.contracts.target import TargetContract
from ingestion.contracts.job import JobContract


class IngestionContract(BaseModel):
    name: str
    job: JobContract
    dataset: DatasetContract
    source: SourceContract
    target: TargetContract
