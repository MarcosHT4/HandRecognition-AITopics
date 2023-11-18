from fastapi import FastAPI
from config import get_settings
from routers import (
    status,
    prediction,
    annotation,
    reports
)

SETTINGS = get_settings()
app = FastAPI(title=SETTINGS.api_name, version=SETTINGS.revision)

app.include_router(status.router)
app.include_router(prediction.router)
app.include_router(annotation.router)
app.include_router(reports.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)