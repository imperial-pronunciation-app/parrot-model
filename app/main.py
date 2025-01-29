from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from allosaurus.app import read_recognizer

from app.routers.phonemes import router as phonemes_router
from app.routers.phonemes import ml_models

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    ml_models["default"] = read_recognizer()
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

app.include_router(phonemes_router)

