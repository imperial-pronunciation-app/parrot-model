
from fastapi import FastAPI

from app.routers.audio_phonemes import router as phonemes_router


app = FastAPI()

app.include_router(phonemes_router)

