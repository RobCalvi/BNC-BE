from typing import List, Optional
from bson import ObjectId
from app.db.database import MongoClient
from app.models.email import Email
from app.repositories.email import EmailRepository


class EmailService:
    def __init__(self, repository: EmailRepository):
        self.repository = repository

    async def create_email(self, client: MongoClient, email: Email) -> Email:
        # Convert company_id to ObjectId
        email.company_id = ObjectId(email.company_id)
        return await self.repository.create(client, email)

    async def list_emails(self, client: MongoClient, skip: int = 0, limit: int = 10) -> List[Email]:
        return await self.repository.list(client, skip, limit)

    async def get_email(self, client: MongoClient, email_id: str) -> Optional[Email]:
        return await self.repository.get(client, email_id)

    async def update_email(self, client: MongoClient, email_id: str, updates: dict) -> bool:
        # Convert company_id to ObjectId if present in updates
        if "company_id" in updates:
            updates["company_id"] = ObjectId(updates["company_id"])
        return await self.repository.update(client, email_id, updates)

    async def delete_email(self, client: MongoClient, email_id: str) -> bool:
        return await self.repository.delete(client, email_id)

    async def get_emails_by_company_id(self, client: MongoClient, company_id: str, skip: int = 0, limit: int = 10) -> List[Email]:
        # Convert company_id to ObjectId
        company_id_obj = ObjectId(company_id)
        return await self.repository.get_emails_by_company_id(client, company_id_obj, skip, limit)
