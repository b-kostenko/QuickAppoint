import uvicorn
from fastapi import FastAPI

from src.api import router
from src.settings import settings

app = FastAPI(
    title="Appointment",
    description="",
    version="1.0.0"
)



@app.get("/health-check")
async def health_check():
    return {"status": "healthy"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=8000,
        reload=True,
        log_level="info"
    )
