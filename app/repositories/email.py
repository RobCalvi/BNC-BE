from typing import List
from bson import ObjectId
from app.db.database import MongoClient
from app.models.email import Email

collection = "emails"


class EmailRepository:

    @staticmethod
    async def create(client: MongoClient, email: Email) -> Email:
        # Convert company_id from string to ObjectId for insertion
        email_dict = email.dict(exclude={"id"})
        email_dict["company_id"] = ObjectId(email_dict["company_id"])  # Convert to ObjectId
        result = await client.collection(collection).insert_one(email_dict)
        email_dict["id"] = str(result.inserted_id)  # Add the inserted ID as a string
        email_dict["company_id"] = str(email_dict["company_id"])  # Convert ObjectId back to string for the response
        return Email(**email_dict)  # Use Pydantic to validate the returned data

    @staticmethod
    async def list(client: MongoClient, skip: int = 0, limit: int = 10) -> List[Email]:
        documents = client.collection(collection).find().skip(skip).limit(limit)
        emails = [
            Email(**{
                **doc,
                "id": str(doc["_id"]),
                "company_id": str(doc["company_id"])  # Convert ObjectId to string
            })
            async for doc in documents
        ]
        return emails


    @staticmethod
    async def get(client: MongoClient, email_id: str) -> Email:
        document = await client.collection(collection).find_one({"_id": ObjectId(email_id)})
        if document:
            document["id"] = str(document["_id"])
            document["company_id"] = str(document["company_id"])  # Convert ObjectId to string for response
            return Email(**document)
        return None

    @staticmethod
    async def update(client: MongoClient, email_id: str, updates: dict) -> bool:
        # Convert company_id in updates if it exists
        if "company_id" in updates:
            updates["company_id"] = ObjectId(updates["company_id"])
        result = await client.collection(collection).update_one({"_id": ObjectId(email_id)}, {"$set": updates})
        return result.matched_count > 0

    @staticmethod
    async def delete(client: MongoClient, email_id: str) -> bool:
        result = await client.collection(collection).delete_one({"_id": ObjectId(email_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_emails_by_company_id(client: MongoClient, company_id: str, skip: int = 0, limit: int = 10) -> List[Email]:
        # Convert `company_id` to `ObjectId` for querying MongoDB
        documents = client.collection(collection).find({"company_id": ObjectId(company_id)}).skip(skip).limit(limit)
        emails = [
            Email(**{**doc, "id": str(doc["_id"]), "company_id": str(doc["company_id"])})
            async for doc in documents
        ]
        return emails
