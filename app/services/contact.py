from app.repositories.contact import ContactRepository
from app.db.database import MongoClient
from app.models.payloads import PostContactPayload
from app.models.contacts import Contact
from typing import List
from app.utils.id_gen import generate_uuid_v4_without_special_chars
from app.enums.operation import LogType
from .change_log import ChangelogService
from datetime import datetime


user = "<example user>"


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository
        
    async def create_contact(self, client: MongoClient, company_id: str, payload: PostContactPayload) -> List[Contact] | None:
        action = Contact(**payload.model_dump(by_alias=True), id=generate_uuid_v4_without_special_chars())
        result = await self.repository.create(client, company_id, action)
        if result:
            await ChangelogService.create_log(
                client,
                ChangelogService.generate_log(LogType.CREATE_CONTACT, payload.model_dump(by_alias=True), datetime.now(), user)
            )
            return await self.repository.list(client, company_id)
        return None


    async def update_contact(self, client: MongoClient, company_id: str, contact_id: str, payload: PostContactPayload) -> List[Contact] | None:
        updates = payload.model_dump(exclude={"id"})  # Exclude the `id` field
        result = await self.repository.update(client, company_id, contact_id, updates)
        if result:
            await ChangelogService.create_log(
                client,
                ChangelogService.generate_log(LogType.UPDATE_CONTACT, updates, datetime.now(), user)
            )
            return await self.repository.list(client, company_id)
        return None


    async def delete_contact(self, client: MongoClient, company_id: str, contact_id: str) -> List[Contact] | None:
        result = await self.repository.delete(client, company_id, contact_id)
        if result:
            await ChangelogService.create_log(client, ChangelogService.generate_log(LogType.DELETE_CONTACT, {"company_id": company_id, "contact_id": contact_id}, datetime.now(), user))
            return await self.repository.list(client, company_id)
        return None
