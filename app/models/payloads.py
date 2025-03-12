from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.action import ActionBase
from datetime import datetime


class FinancialsUpdatePayload(BaseModel):
    checking_account: Optional[float] = Field(None, alias="checkingAccount")
    long_term_investments: Optional[float] = Field(None, alias="longTermInvestments")
    total_investments: Optional[float] = Field(None, alias="totalInvestments")
    loans: Optional[float] = None
    total_donations: Optional[float] = Field(None, alias="totalDonations")
    total_revenue: Optional[float] = Field(None, alias="totalRevenue")
    physical_assets: Optional[float] = Field(None, alias="physicalAssets")



class UpdateCompanyPayload(BaseModel):
    # Existing fields
    legal_name: Optional[str] = Field(None, alias="legalName")
    company_phone_number: Optional[str] = Field(None, alias="companyPhoneNumber")
    company_email: Optional[str] = Field(None, alias="companyEmail")
    company_website: Optional[str] = Field(None, alias="companyWebsite")
    description: Optional[str] = None
    street_address: Optional[str] = Field(None, alias="streetAddress")
    city: Optional[str] = None
    state_or_province: Optional[str] = Field(None, alias="stateOrProvince")
    postal_code: Optional[str] = Field(None, alias="postalCode")
    
    # New/updated top-level fields
    is_active: Optional[bool] = Field(None, alias="isActive")
    is_existing_client: Optional[bool] = Field(None, alias="isExistingClient")
    added_date: Optional[str] = Field(None, alias="addedDate")
    
    # Nested financials object
    financials: Optional[FinancialsUpdatePayload] = None


class PostContactPayload(BaseModel):
    first_name: str = Field(..., alias="firstName", serialization_alias="firstName")  # Maps both input and output
    last_name: str = Field(..., alias="lastName", serialization_alias="lastName")    # Maps both input and output
    email: str
    phone_number: Optional[str] = Field(None, alias="phoneNumber", serialization_alias="phoneNumber")
    gender: Optional[str] = None  # Optional field for gender
    notes: Optional[List[str]] = None         # Default to an empty list


class CreateActionPayload(ActionBase):
    reminder: Optional[str] = None


class CreateReminderPayload(BaseModel):
    company_id: str = Field(..., serialization_alias="companyId", alias="companyId")
    action_id: str = Field(..., serialization_alias="actionId", alias="actionId")
    due_date: datetime = Field(..., serialization_alias="dueDate", alias="dueDate")
