# config/models.py

from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated

from domain.enums import StoreId


Percentage = Annotated[float, Field(ge=0, le=1)]


class IdFormat(BaseModel):
    style: Literal["uuid", "integer", "ret_prefixed"]
    prefix: str = ""


class IdConfig(BaseModel):
    user_id: IdFormat
    order_id: IdFormat
    product_id: IdFormat
    product_id_legacy: IdFormat | None = None
    clickstream_event_id: IdFormat | None = None
    order_event_id: IdFormat | None = None
    session_id: IdFormat | None = None
    anonymous_id: IdFormat | None = None
    return_id: IdFormat | None = None


class NullRates(BaseModel):
    rates: dict[str, Percentage] = Field(default_factory=dict)


class FieldCorruptRates(BaseModel):
    email: float = Field(default=0.0, ge=0, le=1)


class PipelineConfig(BaseModel):
    null_rates: NullRates
    field_corrupt_rates: FieldCorruptRates
    duplication_rate: float = 0.
    legacy_rate: float = 0.


class StoreConfig(BaseModel):
    store_id: StoreId

    ids: IdConfig

    minio_bucket_name: str | None = None

    state_path: Optional[str] = None

    clock_drift_seconds: int = 0
    encoding: str = "utf-8"

    pipeline_config: PipelineConfig | None = None
    async_generators: list[str] | None = None
