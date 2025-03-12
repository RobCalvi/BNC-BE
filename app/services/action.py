from app.repositories.action import ActionRepository
from datetime import datetime
from app.utils.id_gen import generate_uuid_v4_without_special_chars
from app.models.action import Action
from app.models.payloads import CreateActionPayload
from app.db.database import MongoClient
from typing import List
from .change_log import ChangelogService
from .reminder import ReminderService
from app.enums.operation import LogType
from app.models.reminder import ReminderBase


user = "<EXAMPLE USER>"


class ActionService:
    def __init__(self, repository: ActionRepository):
        self.repository = repository

    async def create_action(self, client: MongoClient, company_id: str, payload: CreateActionPayload) -> List[Action] | None:
        now = datetime.now()
        action_id = generate_uuid_v4_without_special_chars()
        result = await self.repository.create(client, company_id, Action(**payload.model_dump(), user=user, date=now,id=action_id))
        if result:
            if payload.reminder:
                try:
                    await ReminderService.create(client, ReminderBase(company_id=company_id, action_id=action_id, due_date=payload.reminder))
                except Exception as ex:
                    print(ex)
            await ChangelogService.create_log(client, ChangelogService.generate_log(LogType.CREATE_ACTION, payload, now, user))
            return await self.repository.list(client, company_id)
        return None

    async def delete_action(self, client: MongoClient, company_id: str, action_id: str) -> List[Action] | None:
        result = await self.repository.delete(client, company_id, action_id)
        if result:
            await ReminderService.delete(client, company_id, action_id)
            await ChangelogService.create_log(client, ChangelogService.generate_log(LogType.DELETE_ACTION, {"company_id": company_id, "action_id": action_id}, datetime.now(), user))
            return await self.repository.list(client, company_id)
        return None

    async def list_actions(self, client: MongoClient, company_id: str) -> List[Action]:
        return await self.repository.list(client, company_id)
