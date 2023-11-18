from pydantic import BaseModel
from schemas.detection import Detection

class Execution(BaseModel):
    time_in_seconds:float