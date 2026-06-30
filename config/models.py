# config/models.py

from pydantic import BaseModel, Field
from typing import Literal, Optional

from domain.enums import StoreId


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
    user: float = Field(default=0.0, ge=0, le=1)
    session_id: float = Field(default=0.0, ge=0, le=1)
    phone: float = Field(default=0.0, ge=0, le=1)
    # tax_amount: float = Field(default=0.0, ge=0, le=1)
    date_of_birth: float = Field(default=0.0, ge=0, le=1)


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

    currencies: list[str]
    state_path: Optional[str] = None

    clock_drift_seconds: int = 0
    encoding: str = "utf-8"

    pipeline_config: PipelineConfig | None = None
