from app.db import MongoClient
from app.models.reminder import Reminder
from typing import Optional, Dict, List
from bson import ObjectId

collection = "reminders"

class ReminderRepository:
    @staticmethod
    async def create(client: MongoClient, payload: Reminder) -> bool:
        res = await client.collection(collection).update_one(
            {
                "company_id": payload.company_id, 
                "action_id": payload.action_id
            }, 
            {"$set": payload.model_dump()}, 
            upsert=True
        )
        return bool(res.upserted_id or res.modified_count > 0)

    @staticmethod
    async def get(client: MongoClient, company_id: str, action_id: str) -> Reminder | None:
        res = await client.collection(collection).find_one(
            {"company_id": company_id, "action_id": action_id}
        )
        return Reminder(**res) if res else None

    @staticmethod
    async def delete(client: MongoClient, company_id: str, action_id: str) -> bool:
        res = await client.collection(collection).delete_one(
            {"company_id": company_id, "action_id": action_id}
        )
        return res.deleted_count > 0

    @staticmethod
    async def complete_reminder(client: MongoClient, reminder_id: str) -> bool:
        res = await client.collection(collection).update_one(
            {"_id": ObjectId(reminder_id)}, 
            {"$set": {"completed": True}}
        )
        return res.modified_count > 0

    @staticmethod
    async def list(client: MongoClient, limit: int, filter: Optional[Dict] = None) -> List[Reminder]:
        _filter = {} if filter is None else filter
        docs = client.collection(collection).find(_filter).limit(limit)
        return [Reminder(**doc) async for doc in docs]

    # NEW: partial update by reminderId
    @staticmethod
    async def update_partial(client: MongoClient, reminder_id: str, updates: Dict) -> Optional[Reminder]:
        """
        Perform a partial update on the reminder identified by `reminder_id`,
        returning the updated document as a Reminder object.
        """
        # Map front-end fields to DB fields if needed.
        # For example, 'dueDate' -> 'due_date', 'isCompleted' -> 'completed'
        field_map = {
            "dueDate": "due_date",
            "isCompleted": "completed",
            # If you want to allow partial updates of 'companyId', 'actionId', etc.,
            # you can add them here as well.
            "companyId": "company_id",
            "actionId": "action_id",
        }

        update_doc = {}
        for key, value in updates.items():
            mapped_key = field_map.get(key)
            if mapped_key:
                update_doc[mapped_key] = value

        if not update_doc:
            # No valid fields to update
            return None

        res = await client.collection(collection).update_one(
            {"_id": ObjectId(reminder_id)},
            {"$set": update_doc}
        )
        # If no reminder was modified (i.e., reminder not found), return None
        if res.matched_count == 0:
            return None

        # Now, fetch the updated doc
        updated_doc = await client.collection(collection).find_one({"_id": ObjectId(reminder_id)})
        return Reminder(**updated_doc) if updated_doc else None
