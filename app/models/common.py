from pydantic import BaseModel, Field, ConfigDict
from .pyobject_id import PyObjectId


class FlexiblePyObjectDoc(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", serialization_alias="id")
    model_config = ConfigDict(extra="allow")
