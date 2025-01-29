
from fastapi import FastAPI

from app.routers.audio_phones import router as phonemes_router
from app.utils.model import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(phonemes_router)

