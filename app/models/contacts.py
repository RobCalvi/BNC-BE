from pydantic import BaseModel, Field
from typing import Optional, List

class Contact(BaseModel):
    id: str
    first_name: Optional[str] = Field(None, alias="firstName", serialization_alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName", serialization_alias="lastName")
    gender: Optional[str] = None
    email: Optional[str] = None
    potential: Optional[bool] = Field(None, alias="potential", serialization_alias="potential")
    dont_bother: Optional[bool] = Field(None, alias="dontBother", serialization_alias="dontBother")
    phone_number: Optional[str] = Field(None, alias="phoneNumber", serialization_alias="phoneNumber")
    is_primary: Optional[bool] = Field(None, alias="isPrimary", serialization_alias="isPrimary")
    notes: Optional[List[str]] = None  # Default to an empty list

