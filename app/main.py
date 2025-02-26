
from fastapi import FastAPI
from app.utils.model import lifespan

from app.routers.audio_phonemes import router as phonemes_router

app = FastAPI(lifespan=lifespan)

app.include_router(phonemes_router)

