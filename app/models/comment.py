from pydantic import BaseModel, Field
from datetime import datetime


class Comment(BaseModel):
    id: str
    content: str
    date: datetime
    user: str
