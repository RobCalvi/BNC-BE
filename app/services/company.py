from fastapi import UploadFile
from typing import List, Optional, Dict
from app.models.company import Company, CompanyBase
from app.repositories.company import CompanyRepository
from app.db.database import MongoClient
from app.models.payloads import UpdateCompanyPayload
from app.enums.operation import LogType
from .change_log import ChangelogService
from datetime import datetime
from app.utils.company.company_excel_util import CompanyExcelUtil

user = "<example user>"


class CompanyService:
    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    async def create_company(self, client: MongoClient, company: Company) -> Company:
        return await self.repository.create(client, company)

    async def list_companies(self, client: MongoClient, skip: int = 0, limit: int = 10) -> List[CompanyBase]:
        return await self.repository.list(client, skip, limit)

    async def list_with_projection(self, client: MongoClient, filter: Dict, projection: Dict,
                                   limit: int | None) -> Dict:
        return await self.repository.list_with_projection(client, filter, projection, limit)

    async def get_company(self, client: MongoClient, company_id: str) -> Optional[Company]:
        return await self.repository.get(client, company_id)

    async def update_company(self, client: MongoClient, company_id: str, payload: UpdateCompanyPayload) -> Optional[Company]:
        # 1) Convert the payload into a dict
        fields = payload.model_dump().items()
        updates = {}
        print(fields)

        # 2) Extract "financials" separately from the rest
        new_financials_data = None
        for name, value in fields:
            if value is not None:
                if name == "financials":
                    # This is your partial (or entire) financial object
                    new_financials_data = value  # e.g. {"checkingAccount": 5000, ...}
                else:
                    updates[name] = value

        # 3) If there ARE top-level updates, do a normal "$set"
        if updates:
            result = await self.repository.update(client, {"$set": updates}, company_id=company_id)
            if not result:
                return None

        # 4) If new_financials_data is present, handle it specially
        if new_financials_data is not None:
            if "timestamp" not in new_financials_data or new_financials_data["timestamp"] is None:
                new_financials_data["timestamp"] = datetime.utcnow().isoformat()
            # EITHER append a new snapshot to the array:
            await self.repository.append_financials_snapshot(
                client,
                company_id,
                new_financials_data
            )
            # Or update the last entry instead of appending, depending on your needs

        # 5) Return the updated company
        await ChangelogService.create_log(
            client,
            ChangelogService.generate_log(LogType.UPDATE_DETAIL, updates={"company_id": company_id, "updates":updates}, date=datetime.now(), user=user)
        )
        return await self.repository.get(client, company_id)


    async def delete_company(self, client: MongoClient, company_id: str) -> bool:
        return await self.repository.delete(client, company_id)

    async def import_companies(self, client: MongoClient, file: UploadFile) -> List[CompanyBase]:
        companies = await self.list_with_projection(client, {}, {"legal_name": 1}, None)
        await CompanyExcelUtil(client, self.repository).parse_imported_data(file, companies)
        await ChangelogService.create_log(client, ChangelogService.generate_log(LogType.IMPORT_COMPANIES, {}, datetime.now(), "TEST USER"))
        # arbitrary large limit until pagination
        return await self.repository.list(client, 0, 10000000)
    
    async def list_companies_with_latest_email(self, client: MongoClient, skip: int = 0, limit: int = 10) -> List[CompanyBase]:
        return await self.repository.list_with_latest_email(client, skip, limit)

