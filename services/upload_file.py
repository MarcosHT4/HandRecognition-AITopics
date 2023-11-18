from fastapi import (
    UploadFile,
    HTTPException,
)
from detector import HandsDetector
from PIL import (
    Image,
    UnidentifiedImageError
)
import io
import numpy as np
from schemas.detection import Detection

class UploadFileService:
    
    def detect_uploadfile(self,detector: HandsDetector, file:UploadFile) -> tuple[Detection, np.ndarray]:
        img_stream = io.BytesIO(file.file.read())
        try:
            img_obj = Image.open(img_stream)
        except UnidentifiedImageError as e:
            raise HTTPException(status_code=415, detail=f"not supported: {e}")
        img_array = np.array(img_obj)
        return detector.detect_image(img_array), img_array