from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.contacts import Contact
from app.models.payloads import PostContactPayload
from app.services.contact import ContactService
from .dependencies import get_contact_service
from app.db import get_mongo_client
from app.db.database import MongoClient
from typing import List


router = APIRouter(
    prefix="/contacts",
    tags=["Contact"]
)


@router.post("", response_model=List[Contact], status_code=status.HTTP_201_CREATED)
async def create_contact(
    payload: PostContactPayload,
    company_id: str = Query(..., alias="companyId"),
    service: ContactService = Depends(get_contact_service),
    client: MongoClient = Depends(get_mongo_client)
):
    result = await service.create_contact(client, company_id, payload)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not complete request.")
    return result



@router.patch("", response_model=List[Contact])
async def update_contact(payload: PostContactPayload, company_id: str = Query(..., alias="companyId"), contact_id: str = Query(..., alias="contactId"), service: ContactService = Depends(get_contact_service), client: MongoClient = Depends(get_mongo_client)):
    result = await service.update_contact(client, company_id, contact_id, payload)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not complete request.")
    return result


@router.delete("/{company_id}/{contact_id}", response_model=List[Contact])
async def update_contact(company_id: str, contact_id: str, service: ContactService = Depends(get_contact_service), client: MongoClient = Depends(get_mongo_client)):
    result = await service.delete_contact(client, company_id, contact_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not complete request.")
    return result
