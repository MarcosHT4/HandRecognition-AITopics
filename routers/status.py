from fastapi import (
    APIRouter,
)
from schemas.status import Status
router = APIRouter()

@router.get("/status")
def get_status() -> Status:
    return Status()

