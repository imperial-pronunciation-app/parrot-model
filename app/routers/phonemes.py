from typing import Dict
from fastapi import APIRouter, UploadFile
from allosaurus.app import read_recognizer

from app.schemas.phonemes import PhonemeResponse

router = APIRouter()
ml_models: Dict[str, None] = {}

@router.post("/api/v1/phonemes", response_model = PhonemeResponse)
async def phonemes(wav: UploadFile):
    recognizer = read_recognizer()
    return recognizer.phonemes(phonemes)