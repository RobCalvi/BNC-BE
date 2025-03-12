from fastapi import Depends
from app.repositories.company import CompanyRepository
from app.services.company import CompanyService
from app.repositories.action import ActionRepository
from app.services.action import ActionService
from app.repositories.contact import ContactRepository
from app.services.contact import ContactService
from app.repositories.email import EmailRepository
from app.services.email import EmailService


def get_company_repository():
    return CompanyRepository()


def get_company_service(repo: CompanyRepository = Depends(get_company_repository)) -> CompanyService:
    return CompanyService(repo)


def get_action_repository():
    return ActionRepository()


def get_action_service(repo: ActionRepository = Depends(get_action_repository)) -> ActionService:
    return ActionService(repo)


def get_contact_repository():
    return ContactRepository()


def get_contact_service(repo: ContactRepository = Depends(get_contact_repository)) -> ContactService:
    return ContactService(repo)


def get_email_service() -> EmailService:
    repository = EmailRepository()
    return EmailService(repository)
