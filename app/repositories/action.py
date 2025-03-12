from typing import List
from app.db.database import MongoClient
from app.models.action import Action
from bson import ObjectId


collection = "company"


class ActionRepository:

    @staticmethod
    async def create(client: MongoClient, company_id: str, action: Action) -> bool:
        result = await client.collection(collection).update_one(
            {"_id": ObjectId(company_id)},
            {"$push": {"actions": action.model_dump()}}
        )
        return result.modified_count > 0

    @staticmethod
    async def list(client: MongoClient, company_id: str) -> List[Action]:
        cursor = client.collection(collection).find({"_id": ObjectId(company_id)}, {'actions': 1, '_id': 0})
        return [Action(**action) async for doc in cursor for action in doc.get('actions', [])]

    @staticmethod
    async def delete(client: MongoClient, company_id: str, action_id: str) -> bool:
        # todo - on delete action delete all of its reminders
        result = await client.collection(collection).update_one(
            {'_id': ObjectId(company_id)},
            {'$pull': {'actions': {'id': action_id}}}
        )
        return result.modified_count > 0
