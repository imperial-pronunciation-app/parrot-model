from fastapi import APIRouter, UploadFile

from app.schemas.pronunciation_inference import PronunciationInferenceResponse
from app.services.audio_processing import create_wav_file, process_audio, whisper_trim
from app.services.inference import infer_phonemes
from config.config import GARBAGE_DETECTABLE_LANGUAGES, Language


router = APIRouter()

@router.post("/api/v1/{lang}/pronunciation_inference", response_model=PronunciationInferenceResponse)
async def phonemes(lang: Language, audio_file: UploadFile) -> PronunciationInferenceResponse:
    audio_bytes = await audio_file.read()
    wav_file = create_wav_file(audio_bytes)

    if lang in GARBAGE_DETECTABLE_LANGUAGES:
        words = whisper_trim(wav_file)
        if not words:
            return PronunciationInferenceResponse(words=[], phonemes=[], success=False)
    else:
        words = None

    process_audio(wav_file)

    return PronunciationInferenceResponse(words=words, phonemes=infer_phonemes(wav_file, lang), success=True)
