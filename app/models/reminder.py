from pydantic import BaseModel, Field
from datetime import datetime
from app.enums.reminder import ReminderState
from app.models.action import Action
from typing import Optional
from .pyobject_id import PyObjectId


class ReminderBase(BaseModel):
    company_id: str = Field(..., serialization_alias="companyId")
    action_id: str = Field(..., serialization_alias="actionId")
    due_date: datetime = Field(..., serialization_alias="dueDate")


class Reminder(ReminderBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", serialization_alias="id")
    created_at: datetime = Field(..., serialization_alias="createdAt")
    completed: Optional[bool] = False


class ReminderDisplay(BaseModel):
    id: str
    company_name: str = Field(..., serialization_alias="companyName")
    is_completed: bool = Field(..., serialization_alias="isCompleted")
    state: ReminderState
    created_at: datetime = Field(..., serialization_alias="createdAt")
    due_date: datetime = Field(..., serialization_alias="dueDate")
    action: Action
