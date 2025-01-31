from typing import Dict

from allosaurus.app import read_recognizer  # noqa: F401
from fastapi import APIRouter, UploadFile

from app.schemas.audio_phones import PhoneResponse


router = APIRouter()
ml_models: Dict[str, None] = {}

@router.post("/api/v1/phones", response_model = PhoneResponse)
async def phones(wav: UploadFile) -> PhoneResponse:
    # recognizer = read_recognizer()
    # return recognizer.phonemes(phonemes)
    return PhoneResponse(phones = ["a", "b", "c"], confidence = [0.9, 0.9, 0.9])

@router.get("/api/v1/phones", response_model = PhoneResponse)
async def get_phonemes() -> PhoneResponse:
    return PhoneResponse(phones = ["a", "b", "c"], confidence = [0.9, 0.9, 0.9])