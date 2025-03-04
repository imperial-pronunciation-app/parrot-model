from argparse import Namespace
from typing import List

from allosaurus.app import read_recognizer

from app.schemas.audio_phonemes import InferWordPhonemesResponse
from app.services.audio_processing import process_audio, whisper_trim
from config.config import MODELS_FOR_LANGUAGES


def get_inference_config(lang: str) -> Namespace:
    """Returns inference configuration based on the language."""
    return Namespace(
        model=MODELS_FOR_LANGUAGES[lang], 
        lang_id=lang,
        prior=None,
        device_id=-1,
        approximate=False
    )


def infer_phonemes(wav_file: str, lang: str) -> List[str]:
    """Performs phoneme inference using the recognizer model."""
    inference_config = get_inference_config(lang)
    
    recognizer = read_recognizer(inference_config_or_name=inference_config)
    return str(recognizer.recognize(wav_file, lang_id=lang)).split(" ")


def infer_word_and_phonemes(
    wav_file: str, 
    lang: str
) -> InferWordPhonemesResponse:
    words = whisper_trim(wav_file)
    if not words:
        return InferWordPhonemesResponse(words=[], phonemes=[], success=False)

    process_audio(wav_file)

    return InferWordPhonemesResponse(words=words, phonemes=infer_phonemes(wav_file, lang), success=True)