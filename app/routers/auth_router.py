from fastapi import APIRouter
from .company import router as company_router
from .action import router as action_router
from .contact import router as contact_router
from .reminder import router as reminder_router
from .email import router as email_router


router = APIRouter(
    prefix="/api/v1"
)

router.include_router(company_router)
router.include_router(action_router)
router.include_router(contact_router)
router.include_router(reminder_router)
router.include_router(email_router)
