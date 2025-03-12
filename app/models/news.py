from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class News(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    link: Optional[str] = None
    date: Optional[datetime | str] = None
