
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import whisper
from fastapi import FastAPI

from app.services.audio_processing import ml_models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    ml_models["whisper"] = whisper.load_model("tiny.en")
    yield
    ml_models.clear()