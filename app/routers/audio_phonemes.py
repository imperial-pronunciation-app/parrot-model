from fastapi import APIRouter, HTTPException, UploadFile

from app.schemas.audio_phonemes import InferWordPhonemesResponse
from app.services.audio_processing import create_wav_file
from app.services.inference import infer_word_and_phonemes
from config.config import SUPPORTED_LANGUAGES


router = APIRouter()

@router.post("/api/v1/{lang}/infer_word_phonemes", response_model=InferWordPhonemesResponse)
async def phonemes(lang: str, audio_file: UploadFile) -> InferWordPhonemesResponse:
    if lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{lang}'. Supported languages: {SUPPORTED_LANGUAGES}"
        )

    audio_bytes = await audio_file.read()
    wav_file = create_wav_file(audio_bytes)
    
    return infer_word_and_phonemes(wav_file, lang)
