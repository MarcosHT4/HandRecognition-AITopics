from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)
from fastapi.responses import Response
from schemas.detection import Detection
from schemas.execution import Execution
from schemas.model_output import ModelOutput
from config import get_settings
from detector import HandsDetector
import time
from services.upload_file import UploadFileService
from services.annotate_image import AnnotateImage
from services.csv_filler import CSVFillerService

router = APIRouter()
hands_detector = HandsDetector()
upload_file_service = UploadFileService()
annotate_image_service = AnnotateImage()
csv_filler_service = CSVFillerService()
SETTINGS = get_settings()

def get_detector():
    return hands_detector
def get_upload_file():
    return upload_file_service
def get_annotate_image():
    return annotate_image_service
def get_csv_filler():
    return csv_filler_service

@router.post("/annotate_image")
def annotate_image(file:UploadFile = File(...), detector = Depends(get_detector), upload_file = Depends(get_upload_file), annotate_image = Depends(get_annotate_image), csv_filler = Depends(get_csv_filler)) -> Response:
    start = time.time()
    detection, img_array = upload_file.detect_uploadfile(detector, file)
    annotated_image = annotate_image.annotate(img_array, detection)
    execution = Execution(time_in_seconds=time.time() - start, detection=detection, img_name=file.filename, img_size=file.size, version_number=SETTINGS.revision)
    output = ModelOutput(execution=execution, detection=detection)
    csv_filler.add_csv_prediction(output, file)
    return Response(content=annotated_image.read(), media_type="image/jpeg")