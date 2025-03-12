from fastapi import HTTPException, status
from app.repositories.reminder import ReminderRepository
from app.models.reminder import ReminderBase, Reminder, ReminderDisplay, ReminderState
from datetime import datetime
from app.db import MongoClient
from .company import CompanyService
from bson import ObjectId
from typing import List


class ReminderService:

    @staticmethod
    async def create(client: MongoClient, payload: ReminderBase) -> Reminder | None:
        now = datetime.now()
        if payload.due_date <= now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Due date cannot be in the past.")
        res = await ReminderRepository.create(client, Reminder(**payload.model_dump(), created_at=now))
        if res:
            return await ReminderRepository.get(client, payload.company_id, payload.action_id)
        return None

    @staticmethod
    async def delete(client: MongoClient, company_id: str, action_id: str):
        return await ReminderRepository.delete(client, company_id, action_id)

    @staticmethod
    async def list_reminders_with_company(client: MongoClient, company_service: CompanyService, limit: int) -> List[ReminderDisplay]:
        now = datetime.now()
        reminders = await ReminderRepository.list(client, limit, {"completed": False})
        ids = list(map(lambda reminder: ObjectId(reminder.company_id), reminders))
        _filter = {
            '_id': {'$in': ids}
        }
        projection = {
            "actions": 1,
            "legal_name": 1
        }
        companies = await company_service.list_with_projection(client, _filter, projection, limit)
        reminder_list = []
        for reminder in reminders:
            if reminder.company_id in companies:
                reminder_action = [action for action in companies[reminder.company_id].actions if action["id"] == reminder.action_id]
                if len(reminder_action) == 1:
                    reminder_list.append(
                        ReminderDisplay(
                            id=str(reminder.id),
                            company_name=companies[reminder.company_id].legal_name,
                            is_completed=reminder.completed,
                            created_at=reminder.created_at,
                            due_date=reminder.due_date,
                            action=reminder_action[0],
                            state=ReminderState.PAST if now > reminder.due_date else ReminderState.NOT_PAST
                        )
                    )
        return reminder_list

    @staticmethod
    async def list(client: MongoClient, limit: int):
        return await ReminderRepository.list(client, limit)

    @staticmethod
    async def complete(client: MongoClient, reminder_id: str) -> bool:
        return await ReminderRepository.complete_reminder(client, reminder_id)
