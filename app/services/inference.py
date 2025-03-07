from argparse import Namespace
from typing import List

from allosaurus.app import read_recognizer

from config.config import MODELS_FOR_LANGUAGES, Language


def get_inference_config(lang: Language) -> Namespace:
    """Returns inference configuration based on the language."""
    return Namespace(
        model=MODELS_FOR_LANGUAGES[lang], 
        lang_id=lang,
        prior=None,
        device_id=-1,
        approximate=False
    )


def infer_phonemes(wav_file: str, lang: Language) -> List[str]:
    """Performs phoneme inference using the recognizer model."""
    inference_config = get_inference_config(lang)
    
    recognizer = read_recognizer(inference_config_or_name=inference_config)
    return str(recognizer.recognize(wav_file, lang_id=lang)).split(" ")
