from fastapi import APIRouter, Depends, Query, HTTPException, status, Path
from app.db import MongoClient, get_mongo_client
from app.models.reminder import ReminderDisplay, ReminderBase, Reminder
from app.services.reminder import ReminderService
from typing import Optional, List
from .dependencies import get_company_service
from app.models.payloads import CreateReminderPayload

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"]
)


@router.get("", response_model=List[ReminderDisplay])
async def list_reminders(limit: Optional[int] = Query(20), client: MongoClient = Depends(get_mongo_client), company_service = Depends(get_company_service)):
    return await ReminderService.list_reminders_with_company(client, company_service, limit)


@router.post("", response_model=Reminder, status_code=status.HTTP_201_CREATED)
async def create_reminder(payload: CreateReminderPayload, client: MongoClient = Depends(get_mongo_client)):
    reminder = await ReminderService.create(client, ReminderBase(company_id=payload.company_id, action_id=payload.action_id, due_date=payload.due_date))
    if reminder is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create reminder.")
    return reminder


@router.patch("/complete/{reminder_id}")
async def complete_reminder(reminder_id: str, client: MongoClient = Depends(get_mongo_client)):
    return await ReminderService.complete(client, reminder_id)

