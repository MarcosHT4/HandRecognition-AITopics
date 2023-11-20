from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)
from schemas.execution import Execution
from schemas.model_output import ModelOutput
from config import get_settings
from detector import HandsDetector
import time
from services.upload_file import UploadFileService
from services.csv_filler import CSVFillerService
from functools import cache
router = APIRouter()
hands_detector = HandsDetector()
upload_file_service = UploadFileService()
csv_filler_service = CSVFillerService()
SETTINGS = get_settings()

@cache
def get_detector():
    return hands_detector
@cache
def get_upload_file():
    return upload_file_service
@cache
def get_csv_filler():
    return csv_filler_service


@router.post("/predict")
def detect_image(file:UploadFile = File(...), detector = Depends(get_detector), upload_file = Depends(get_upload_file), csv_filler = Depends(get_csv_filler))-> ModelOutput:
    start = time.time()
    detection, _ = upload_file.detect_uploadfile(detector, file)
    execution = Execution(time_in_seconds=time.time() - start, detection=detection, img_name=file.filename, img_size=file.size, version_number=SETTINGS.revision)
    output = ModelOutput(execution=execution, detection=detection)
    csv_filler.add_csv_prediction(output, file)
    return output