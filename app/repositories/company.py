from datetime import datetime
from typing import List, Optional, Dict
from bson import ObjectId
from app.db.database import MongoClient
from app.models.company import Company, CompanyBase
from app.models.common import FlexiblePyObjectDoc
from pymongo.results import InsertManyResult

collection = "company"


class CompanyRepository:

    @staticmethod
    async def create(client: MongoClient, company: Company) -> Company:
        company_dict = company.dict(exclude={"id"})
        result = await client.collection(collection).insert_one(company_dict)
        company_dict["id"] = result.inserted_id
        return Company(**company_dict)

    @staticmethod
    async def create_many(client: MongoClient, companies: list) -> InsertManyResult:
        return await client.collection(collection).insert_many(companies)

    @staticmethod
    async def list(client: MongoClient, skip: int = 0, limit: int = 10) -> List[CompanyBase]:
        return [
            CompanyBase(**{
                **doc, 
                'financials': doc["financials"][-1], 
                })
            async for doc in client.collection(collection).find().skip(skip).limit(limit)
        ]

    @staticmethod
    async def list_with_projection(client: MongoClient, filter: Dict, projection: Dict, limit: int | None) -> Dict[str, FlexiblePyObjectDoc]:
        return {
            str(doc["_id"]): FlexiblePyObjectDoc(**doc)
            async for doc in client.collection(collection).find(filter, projection).limit(limit if limit is not None else 0)
        }

    @staticmethod
    async def get(client: MongoClient, company_id: str) -> Optional[Company]:
        model_fields = Company.model_fields.keys()  # Ensure only model fields are included
        projection = {field: 1 for field in model_fields}
        projection["financials"] = {"$arrayElemAt": ["$financials", -1]}  # Get the latest financial entry

        pipeline = [
            {"$match": {"_id": ObjectId(company_id)}},
            {"$project": projection},
            # Reformat the contacts array to use camelCase
            {
                "$addFields": {
                    "contacts": {
                        "$map": {
                            "input": "$contacts",
                            "as": "contact",
                            "in": {
                                "id": "$$contact.id",
                                "firstName": "$$contact.first_name",
                                "lastName": "$$contact.last_name",
                                "gender": "$$contact.gender",
                                "email": "$$contact.email",
                                "potential": "$$contact.potential",
                                "dontBother": "$$contact.dont_bother",
                                "phoneNumber": "$$contact.phone_number",
                                "isPrimary": "$$contact.is_primary",
                                "notes": "$$contact.notes",
                            },
                        }
                    }
                }
            },
        ]

        company = [c async for c in client.collection(collection).aggregate(pipeline)]
        if len(company) > 0:
            return Company(**company[0])  # Pydantic will handle serialization
        return None


    @staticmethod
    async def update(client: MongoClient, updates: dict, company_id: Optional[str] = None, legal_name: Optional[str] = None) -> bool:
        if company_id:
            filter_criteria = {"_id": ObjectId(company_id)}
        elif legal_name:
            filter_criteria = {"legal_name": legal_name}
        else:
            raise ValueError("Either 'company_id' or 'legal_name' must be provided.")
        result = await client.collection(collection).update_one(filter_criteria, updates)
        return result.matched_count > 0
    @staticmethod
    
    @staticmethod
    async def get_last_financials_snapshot(client: MongoClient, company_id: str) -> Optional[dict]:
        """
        Returns the *last* snapshot in the 'financials' array, or None if empty.
        """
        doc = await client.collection("company").find_one(
            {"_id": ObjectId(company_id)},
            {"financials": 1}
        )
        if not doc or "financials" not in doc or not doc["financials"]:
            return None
        # The last item
        return doc["financials"][-1]
    
    @staticmethod
    async def append_financials_snapshot(client: MongoClient, company_id: str, partial_data: dict) -> bool:
        # 1) Load the last snapshot
        last_snapshot = await CompanyRepository.get_last_financials_snapshot(client, company_id)

        # 2) If there's no existing snapshot, start from an empty dict
        if not last_snapshot:
            last_snapshot = {}

        # 3) Make a copy to avoid mutating the old snapshot
        new_snapshot = {**last_snapshot}

        # 4) Merge only the non-null fields from partial_data
        for k, v in partial_data.items():
            if v is not None:
                new_snapshot[k] = v
        # That way, if partial_data had "checking_account": None, it won't overwrite the old value.

        # 5) Ensure a timestamp
        if "timestamp" not in new_snapshot or new_snapshot["timestamp"] is None:
            new_snapshot["timestamp"] = datetime.utcnow().isoformat()

        # Optionally store "datetime" or any other field
        new_snapshot["datetime"] = datetime.utcnow().isoformat()

        # 6) Append this new snapshot
        result = await client.collection("company").update_one(
            {"_id": ObjectId(company_id)},
            {"$push": {"financials": new_snapshot}}
        )
        return result.modified_count > 0

    @staticmethod
    async def delete(client: MongoClient, company_id: str) -> bool:
        result = await client.collection(collection).delete_one({"_id": ObjectId(company_id)})
        return result.deleted_count > 0

    @staticmethod
    async def list_with_latest_email(client: MongoClient, skip: int = 0, limit: int = 10) -> List[CompanyBase]:
        pipeline = [
            # Join emails with companies
            {
                "$lookup": {
                    "from": "emails",
                    "localField": "_id",
                    "foreignField": "company_id",
                    "as": "emails"
                }
            },
            # Sort emails by datetime in descending order
            {
                "$addFields": {
                    "emails": {"$sortArray": {"input": "$emails", "sortBy": {"datetime": -1}}}
                }
            },
            # Add latest email details
            {
                "$addFields": {
                    "latest_email_datetime": {"$ifNull": [{"$arrayElemAt": ["$emails.datetime", 0]}, None]},
                    "latest_email_template": {"$ifNull": [{"$arrayElemAt": ["$emails.template", 0]}, None]}
                }
            },
            # Project all required fields for CompanyBase
            {
                "$project": {
                    "_id": 1,
                    "legal_name": 1,
                    "is_active": 1,
                    "is_existing_client": 1,
                    "addedDate": 1,
                    "financials": {"$arrayElemAt": ["$financials", -1]},  # Get the latest financial entry
                    "contacts": 1,
                    "contact_name": {
                        "$reduce": {
                            "input": {
                                "$map": {
                                    "input": {
                                        "$filter": {
                                            "input": "$contacts",
                                            "as": "contact",
                                            "cond": {
                                                "$and": [
                                                    {"$ne": ["$$contact.first_name", ""]},
                                                    {"$ne": ["$$contact.first_name", None]},
                                                    {"$ne": ["$$contact.last_name", ""]},
                                                    {"$ne": ["$$contact.last_name", None]},
                                                    {"$ne": ["$$contact.email", ""]},
                                                    {"$ne": ["$$contact.email", None]}
                                                ]
                                            }
                                        }
                                    },
                                    "as": "contact",
                                    "in": {
                                        "$concat": [
                                            "$$contact.first_name",
                                            " ",
                                            "$$contact.last_name"
                                        ]
                                    }
                                }
                            },
                            "initialValue": "",
                            "in": {
                                "$cond": {
                                    "if": {"$eq": ["$$value", ""]},
                                    "then": "$$this",
                                    "else": {
                                        "$concat": ["$$value", ", ", "$$this"]
                                    }
                                }
                            }
                        }
                    },
                    "latest_email_datetime": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S.%LZ", "date": "$latest_email_datetime"}},
                    "latest_email_template": 1
                }
            },
            # Pagination
            {"$skip": skip},
            {"$limit": limit}
        ]

        return [
            CompanyBase(**doc) async for doc in client.collection(collection).aggregate(pipeline)
        ]
