from fastapi import FastAPI
import uvicorn

from src.settings import settings
from src.api.users import router as user_router


app = FastAPI(
    title="Appointment",
    description="",
    version="1.0.0"
)



@app.get("/health-check")
async def health_check():
    return {"status": "healthy"}


app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=8000,
        reload=True,
        log_level="info"
    )
