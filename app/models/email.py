from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .contacts import Contact

class Email(BaseModel):
    id: str
    datetime: datetime
    sender: str
    recipient: Contact
    template: str
    sent: Optional[datetime] = None
    answered: Optional[datetime] = None
    company_id: str  # Change from ObjectId to str

    class Config:
        arbitrary_types_allowed = True  # Allow ObjectId type
        
        
class EmlRequest(BaseModel):
    subject: str
    to_email: str
    html_body: str
    images: List[str]  # Base64-encoded images

    