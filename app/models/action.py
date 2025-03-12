from datetime import datetime
from pydantic import BaseModel
from app.enums.operation import OperationType


class ActionBase(BaseModel):
    title: str
    description: str
    operation: OperationType


class Action(ActionBase):
    id: str
    date: datetime
    user: str
