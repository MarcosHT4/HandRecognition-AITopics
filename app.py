from fastapi import FastAPI
from config import get_settings
from routers import (
    status,
    prediction,
    annotation,
    reports
)
from fastapi.middleware.cors import CORSMiddleware



SETTINGS = get_settings()
app = FastAPI(title=SETTINGS.api_name, version=SETTINGS.revision)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router)
app.include_router(prediction.router)
app.include_router(annotation.router)
app.include_router(reports.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)