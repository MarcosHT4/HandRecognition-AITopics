from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cache

class Settings(BaseSettings):
    api_name:str = "Hand Detection Service"
    revision:str = "0.0.1"
    model_name:str = "MediaPipe Hand Landmarker"
    model_version:str = "models/hand_landmarker.task"
    csv_path:str = "outputs/predictions.csv"

@cache
def get_settings():
    return Settings()
