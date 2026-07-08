# config/models.py
from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict, field_validator
import re
from typing import Literal, Optional, Annotated

from domain.enums import StoreId


Percentage = Annotated[float, Field(ge=0, le=1)]
_ALLOWED_PLACEHOLDERS = {"store", "entity", "date"}
_PLACEHOLDER_PATTERN = re.compile(r"\{(\w+)\}")


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


class FieldCaseCorruptRates(BaseModel):
    rates: dict[str, Percentage] = Field(default_factory=dict)


class TrailingSpacesCorruptRates(BaseModel):
    rates: dict[str, Percentage] = Field(default_factory=dict)


class PipelineConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    null_rates: NullRates
    field_case_corrupt_rates: FieldCaseCorruptRates
    trailing_spaces_corrupt_rates: TrailingSpacesCorruptRates | None = None
    duplication_rate: float = 0.
    legacy_rate: float = 0.


class OnStartBuildConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_name: str
    num_objects: int


class BreaktimeConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    shape: float = 1.
    scale: float = 1.


class AsyncGenerationConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    breaktime_config: BreaktimeConfig


class StoreConfig(BaseModel):
    store_id: StoreId

    ids: IdConfig

    state_path: Optional[str] = None

    clock_drift_seconds: int = 0
    encoding: str = "utf-8"
    breaktime_config: BreaktimeConfig

    on_start_build: list[OnStartBuildConfig] | None = None
    pipeline_config: PipelineConfig | None = None
    async_generators: list[AsyncGenerationConfig] | None = None


class LakeFormat(StrEnum):
    PARQUET = "parquet"
    DELTA = "delta"


class BucketConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    bucket: str


class LayerConfig(BucketConfig):
    path_template: str
    format: LakeFormat = LakeFormat.PARQUET

    @field_validator("path_template")
    @classmethod
    def _validate_placeholders(cls, v: str) -> str:
        used = set(_PLACEHOLDER_PATTERN.findall(v))
        unknown = used - _ALLOWED_PLACEHOLDERS
        if unknown:
            raise ValueError(
                f"path_template has unknown placeholder(s): {unknown}. "
                f"Allowed: {_ALLOWED_PLACEHOLDERS}"
            )
        return v

    def resolve(self, *, store: str, entity: str, date: str) -> str:
        """Build a concrete object path for a given store/entity/date.

        Only pass what the template actually references; extra kwargs
        are ignored by str.format, missing ones raise KeyError early
        rather than writing to the wrong path silently.
        """
        return self.path_template.format(store=store, entity=entity, date=date)


class LakeConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    landing: BucketConfig
    bronze: LayerConfig
    silver: LayerConfig
