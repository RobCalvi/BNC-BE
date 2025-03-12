from app.db import MongoClient
from app.models.reminder import Reminder
from typing import Optional, Dict, List
from bson import ObjectId

collection = "reminders"


class ReminderRepository:
    @staticmethod
    async def create(client: MongoClient, payload: Reminder) -> bool:
        res = await client.collection(collection).update_one({
            "company_id": payload.company_id, "action_id": payload.action_id
        }, {"$set": payload.model_dump()}, upsert=True)
        print(res)
        return bool(res.upserted_id or res.modified_count > 0)

    @staticmethod
    async def get(client: MongoClient, company_id: str, action_id: str) -> Reminder | None:
        res = await client.collection(collection).find_one({"company_id": company_id, "action_id": action_id})
        if res is not None:
            return Reminder(**res)
        return res

    @staticmethod
    async def delete(client: MongoClient, company_id: str, action_id: str) -> bool:
        res = await client.collection(collection).delete_one({"company_id": company_id, "action_id": action_id})
        return res.deleted_count > 0

    @staticmethod
    async def complete_reminder(client: MongoClient, reminder_id: str) -> bool:
        res = await client.collection(collection).update_one({"_id": ObjectId(reminder_id)}, {"$set": {
            "completed": True}})
        return res.modified_count > 0

    @staticmethod
    async def list(client: MongoClient, limit, filter: Optional[Dict] = None) -> List[Reminder]:
        _filter = {} if filter is None else filter
        return [Reminder(**doc) async for doc in client.collection(collection).find(_filter).limit(limit)]
