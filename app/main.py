
from fastapi import FastAPI

from app.routers.pronunciation_inference import router as pronunciation_inference_router
from app.utils.model import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(pronunciation_inference_router)

