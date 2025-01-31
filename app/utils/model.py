
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from allosaurus.app import read_recognizer
from fastapi import FastAPI

from app.routers.audio_phonemes import ml_models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    ml_models["default"] = read_recognizer()
    yield
    ml_models.clear()