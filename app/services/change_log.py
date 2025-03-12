from app.repositories.changelog import ChangelogRepository
from app.db import MongoClient
from app.models.changelog import Changelog
from app.enums.operation import LogType
from datetime import datetime
from typing import Any


class ChangelogService:
    @staticmethod
    async def create_log(client: MongoClient, log: Changelog):
        try:
            return await ChangelogRepository.insert(client, log)
        except Exception as ex:
            print(ex)

    @staticmethod
    def generate_log(operation: LogType, updates: Any, date: datetime, user: str):
        return Changelog(operation=operation, updates=updates, date=date, user=user)
