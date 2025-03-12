from pydantic import BaseModel
from datetime import datetime
from app.enums.operation import LogType
from typing import Any


class Changelog(BaseModel):
    operation: LogType
    updates: Any
    date: datetime
    user: str
