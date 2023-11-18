import io
import cv2
from fastapi import(
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    status,
    Depends
)
import os
import csv
from functools import cache
from fastapi.responses import Response
import numpy as np
from PIL import Image, UnidentifiedImageError
from config import get_settings
from detector import HandsDetector
from schemas.status import Status
from schemas.execution import Execution
from schemas.model_output import ModelOutput
from schemas.detection import Detection
import time
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions

SETTINGS = get_settings()

app = FastAPI(title=SETTINGS.api_name, version=SETTINGS.revision)
hands_detector = HandsDetector()

def get_detector():
    return hands_detector

def detect_uploadfile(detector: HandsDetector, file:UploadFile):
    img_stream = io.BytesIO(file.file.read())
    try:
        img_obj = Image.open(img_stream)
    except UnidentifiedImageError as e:
        raise HTTPException(status_code=415, detail=f"not supported: {e}")
    img_array = np.array(img_obj)
    return detector.detect_image(img_array), img_array

def annotate(img_array, detection:Detection) -> io.BytesIO:
    annotate_image = img_array.copy()
    for idx,hand in enumerate(detection.landmarks):
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(
                x=landmark[0], y=landmark[1], z=landmark[2]
            )
            for landmark in hand
        ])
        solutions.drawing_utils.draw_landmarks(
            annotate_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style()
        )
        cv2.putText(annotate_image, f"{detection.labels[idx]}", tuple(detection.bbox[idx]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    img_pil = Image.fromarray(annotate_image)
    image_stream = io.BytesIO()
    img_pil.save(image_stream, format="JPEG")
    image_stream.seek(0)
    return image_stream

def add_csv_prediction(modelOutput:ModelOutput, img_file:UploadFile) -> None:
    img_name = img_file.filename
    modelName = SETTINGS.model_name
    modelRevision = SETTINGS.revision
    date_and_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    executionTime = modelOutput.execution.time_in_seconds
    img_size = img_file.size
    prediction = modelOutput.detection.labels
    
    csv_file_path = SETTINGS.csv_path
    is_new_file = not os.path.exists(csv_file_path)
    with open(csv_file_path, "a", newline='') as f:
        writer = csv.writer(f)
        if is_new_file:
            header = ["Image File Name", "Image Size", "Prediction", "Date and Time", "Execution Time", "Model", "Model Revision"]
            writer.writerow(header)
        row=[img_name,img_size,prediction,date_and_time,executionTime,modelName,modelRevision]
        writer.writerow(row)

@app.get("/status")
def get_status() -> Status:
    return Status()


@app.post("/predict")
def detect_image(file:UploadFile = File(...), detector = Depends(get_detector))-> ModelOutput:
    start = time.time()
    detection, img_array = detect_uploadfile(detector, file)
    execution = Execution(time_in_seconds=time.time() - start, detection=detection)
    output = ModelOutput(execution=execution, detection=detection)
    add_csv_prediction(output, file)
    return output

@app.post("/annotate_image")
def annotate_image(file:UploadFile = File(...), detector = Depends(get_detector)) -> Response:
    start = time.time()
    detection, img_array = detect_uploadfile(detector, file)
    annotated_image = annotate(img_array, detection)
    execution = Execution(time_in_seconds=time.time() - start, detection=detection)
    output = ModelOutput(execution=execution, detection=detection)
    add_csv_prediction(output, file)
    return Response(content=annotated_image.read(), media_type="image/jpeg")

@app.get("/reports")
def get_csv_reports() -> Response:
    csv_file_path = SETTINGS.csv_path
    if not os.path.exists(csv_file_path):
        raise HTTPException(status_code=404, detail="CSV File not found")
    with open(csv_file_path, "r") as f:
        csv_content = f.read()
    return Response(content=csv_content, media_type="text/csv")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)