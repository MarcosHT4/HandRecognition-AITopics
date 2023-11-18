from pydantic import BaseModel
from config import get_settings

SETTINGS = get_settings()

class Status(BaseModel):
    api_status:str = "OK"
    api_name:str = SETTINGS.api_name
    version:str = SETTINGS.revision
    model_name:str = SETTINGS.model_name