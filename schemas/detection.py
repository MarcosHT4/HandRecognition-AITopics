from pydantic import BaseModel

class Detection(BaseModel):
    landmarks:list[list[list[float]]]
    labels:list[str]
    bbox:list[list[int]]

