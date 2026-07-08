from enum import StrEnum
from pydantic import BaseModel, ConfigDict, field_validator
import re


_ALLOWED_PLACEHOLDERS = {"store", "entity", "date"}
_PLACEHOLDER_PATTERN = re.compile(r"\{(\w+)\}")


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
