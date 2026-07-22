from pydantic import BaseModel, Field
from typing import Any
    

class SourceContract(BaseModel):
    type: str
    options: dict[str, Any] = Field(default_factory=dict)
