from schemas.model_output import ModelOutput
import csv
import time
from fastapi import UploadFile
from config import get_settings
import os

SETTINGS = get_settings()

class CSVFillerService:
    def add_csv_prediction(self,modelOutput:ModelOutput, img_file:UploadFile) -> None:
        img_name = img_file.filename
        modelName = SETTINGS.model_name
        modelRevision = SETTINGS.revision
        date_and_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        executionTime = modelOutput.execution.time_in_seconds
        img_size = img_file.size
        prediction = modelOutput.detection.labels
        score = modelOutput.detection.scores

        csv_file_path = SETTINGS.csv_path
        if not os.path.exists(csv_file_path.split("/")[0]):
            os.makedirs(csv_file_path.split("/")[0])
        is_new_file = not os.path.exists(csv_file_path)
        with open(csv_file_path, "a", newline='') as f:
            writer = csv.writer(f)
            if is_new_file:
                header = ["Image File Name", "Image Size", "Prediction", "Prediction Score","Date and Time", "Execution Time", "Model", "Model Revision"]
                writer.writerow(header)
            row=[img_name,img_size,prediction,score,date_and_time,executionTime,modelName,modelRevision]
            writer.writerow(row)