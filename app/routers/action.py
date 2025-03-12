from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.action import Action
from app.models.payloads import CreateActionPayload
from app.services.action import ActionService
from .dependencies import get_action_service
from app.db import get_mongo_client
from app.db.database import MongoClient
from typing import List


router = APIRouter(
    prefix="/actions",
    tags=["Actions"]
)


@router.post("", response_model=List[Action], status_code=status.HTTP_201_CREATED)
async def create_action(payload: CreateActionPayload, company_id: str = Query(..., alias="companyId"), service: ActionService = Depends(get_action_service), client: MongoClient = Depends(get_mongo_client)):
    result = await service.create_action(client, company_id, payload)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not complete request.")
    return result


@router.delete("/{company_id}/{action_id}", response_model=List[Action])
async def delete_action(company_id: str, action_id: str,  service: ActionService = Depends(get_action_service), client: MongoClient = Depends(get_mongo_client)):
    result = await service.delete_action(client, company_id, action_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete action.")
    return result
