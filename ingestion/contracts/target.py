from pydantic import BaseModel, Field
from typing import Any


class TargetContract(BaseModel):
    layer: str
    format: str
    mode: str
    options: dict[str, Any] = Field(default_factory=dict)
