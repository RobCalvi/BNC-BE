from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from .pyobject_id import PyObjectId
from .action import Action
from .comment import Comment
from .news import News
from .contacts import Contact
from .financials import Financials
from datetime import date

class CompanyBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", serialization_alias="id")
    legal_name: str = Field(..., serialization_alias="legalName")
    is_active: bool = Field(..., serialization_alias="isActive")
    is_existing_client: bool = Field(..., serialization_alias="isExistingClient")
    addedDate: Optional[date] = Field(None, serialization_alias="addedDate")
    financials: List[Financials] | Financials
    contact_name: Optional[str] = Field(None, serialization_alias="contactName")
    latest_email_datetime: Optional[str] = Field(None, serialization_alias="latestEmailDatetime")
    latest_email_template: Optional[str] = Field(None, serialization_alias="latestEmailTemplate")

    model_config = ConfigDict(
        arbitrary_types_allowed=True, 
        json_encoders={ObjectId: str}, 
        populate_by_name=True
    )


class Company(CompanyBase):
    company_phone_number: str = Field(..., serialization_alias="companyPhoneNumber")
    company_email: str = Field(..., serialization_alias="companyEmail")
    company_website: str = Field(..., serialization_alias="companyWebsite")
    description: str
    fcc: int
    street_address: str = Field(..., serialization_alias="streetAddress")
    city: str
    state_or_province: str = Field(..., serialization_alias="stateOrProvince")
    postal_code: str = Field(..., serialization_alias="postalCode")
    country: str
    contacts: List[Contact] = []
    actions: List[Action] = []
    comments: List[Comment] = []
    news: List[News] = []
