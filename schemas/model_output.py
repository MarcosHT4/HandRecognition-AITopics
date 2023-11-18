from pydantic import BaseModel
from schemas.detection import Detection
from schemas.execution import Execution
class ModelOutput(BaseModel):
    execution:Execution
    detection:Detection