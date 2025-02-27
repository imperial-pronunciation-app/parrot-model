from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, UploadFile

from app.schemas.audio_phonemes import InferPhonemesResponse
from app.services.audio_processing import create_wav_file, process_audio, trim_audio
from app.services.inference import infer_phonemes
from config.config import SUPPORTED_LANGUAGES


router = APIRouter()

@router.post("/api/v1/{lang}/infer_phonemes", response_model=InferPhonemesResponse)
async def phonemes(lang: str, audio_file: UploadFile, attempt_word: Annotated[str, Form()]) -> InferPhonemesResponse:
    if lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{lang}'. Supported languages: {SUPPORTED_LANGUAGES}"
        )

    audio_bytes = await audio_file.read()
    wav_file = create_wav_file(audio_bytes)
    
    trim_audio(wav_file, attempt_word)

    process_audio(wav_file)

    return InferPhonemesResponse(phonemes=infer_phonemes(wav_file, lang))

# for testing
@router.get("/api/v1/phones", response_model = InferPhonemesResponse)
async def get_phonemes() -> InferPhonemesResponse:
    return InferPhonemesResponse(phonemes = ["a", "b", "c"])