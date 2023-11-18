from fastapi import (
    APIRouter,
    HTTPException
)
from fastapi.responses import Response
from config import get_settings
import os

router = APIRouter()
SETTINGS = get_settings()


@router.get("/reports")
def get_csv_reports() -> Response:
    csv_file_path = SETTINGS.csv_path
    if not os.path.exists(csv_file_path):
        raise HTTPException(status_code=404, detail="CSV File not found")
    with open(csv_file_path, "r") as f:
        csv_content = f.read()
    return Response(content=csv_content, media_type="text/csv")