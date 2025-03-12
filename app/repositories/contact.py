from typing import List
from app.db.database import MongoClient
from app.models.contacts import Contact
from bson import ObjectId


collection = "company"


class ContactRepository:

    @staticmethod
    async def create(client: MongoClient, company_id: str, contact: Contact) -> bool:
        # Use default serialization for MongoDB (snake_case)
        result = await client.collection(collection).update_one(
            {"_id": ObjectId(company_id)},
            {"$push": {"contacts": contact.model_dump()}}  # No by_alias=True here
        )
        return result.modified_count > 0


    @staticmethod
    async def list(client: MongoClient, company_id: str) -> List[Contact]:
        cursor = client.collection(collection).find({"_id": ObjectId(company_id)}, {'contacts': 1, '_id': 0})
        return [
            Contact(**{
                **contact,  # Original contact data from MongoDB
                "firstName": contact.get("first_name", ""),  # Handle missing fields
                "lastName": contact.get("last_name", ""),
                "phoneNumber": contact.get("phone_number", ""),
                "isPrimary": contact.get("is_primary", None),
                "notes": contact.get("notes", [])
            })
            async for doc in cursor for contact in doc.get('contacts', [])
        ]


    @staticmethod
    async def update(client: MongoClient, company_id: str, contact_id: str, updates: dict) -> bool:
        # Build the $set dictionary with the correct MongoDB path
        set_updates = {f"contacts.$.{key}": value for key, value in updates.items() if key != "id"}
        result = await client.collection(collection).update_one(
            {'_id': ObjectId(company_id), 'contacts.id': contact_id},  # Match by company ID and contact ID
            {'$set': set_updates}  # Apply the updates
        )
        return result.matched_count > 0


    @staticmethod
    async def delete(client: MongoClient, company_id: str, contact_id: str) -> bool:
        result = await client.collection(collection).update_one(
            {'_id': ObjectId(company_id)},
            {'$pull': {'contacts': {'id': contact_id}}}
        )
        return result.modified_count > 0
