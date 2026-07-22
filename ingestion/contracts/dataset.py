from pydantic import BaseModel

from domain.enums import StoreId, EntityType


class DatasetContract(BaseModel):
    store: StoreId
    entity: EntityType
