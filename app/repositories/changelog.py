from app.db import MongoClient
from app.models.changelog import Changelog


collection = "changelog"


class ChangelogRepository:

    @staticmethod
    async def insert(client: MongoClient, payload: Changelog) -> str | None:
        return (await client.collection(collection).insert_one(payload.model_dump())).inserted_id
