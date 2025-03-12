from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Dict
from app.models.company import Company, CompanyBase
from app.services.company import CompanyService
from .dependencies import get_company_service
from app.db import MongoClient, get_mongo_client
from app.models.payloads import UpdateCompanyPayload

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=Company)
async def create_company(company: Company, service: CompanyService = Depends(get_company_service), client: MongoClient = Depends(get_mongo_client)):
    return await service.create_company(client, company)


@router.get("/", response_model=List[CompanyBase])
async def list_companies(skip: int = 0, limit: int = 10, service: CompanyService = Depends(get_company_service), client: MongoClient = Depends(get_mongo_client)):
    return await service.list_companies_with_latest_email(client, skip, limit)


@router.get("/{company_id}", response_model=Company)
async def get_company(company_id: str, service: CompanyService = Depends(get_company_service), client: MongoClient = Depends(get_mongo_client)):
    company = await service.get_company(client, company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


@router.patch("/{company_id}", response_model=Company)
async def update_company(company_id: str, payload:UpdateCompanyPayload, service: CompanyService = Depends(get_company_service), client: MongoClient = Depends(get_mongo_client)):
    company = await service.update_company(client, company_id, payload)
    if not company:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update company.")
    return company


@router.delete("/{company_id}", response_model=dict)
async def delete_company(company_id: str, service: CompanyService = Depends(get_company_service), client: MongoClient = Depends(get_mongo_client)):
    result = await service.delete_company(client, company_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return {"message": "Company deleted successfully"}


@router.post("/import", status_code=status.HTTP_201_CREATED, response_model=List[CompanyBase])
async def import_companies(file: UploadFile = File(...), service: CompanyService = Depends(get_company_service), client: MongoClient = Depends(get_mongo_client)):
    return await service.import_companies(client, file)
