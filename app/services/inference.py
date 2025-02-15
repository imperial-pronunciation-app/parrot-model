import json
from argparse import Namespace
from typing import Dict, List, cast

from allosaurus.app import read_recognizer

from config.config import MODELS_FOR_LANGUAGES


def get_inference_config(lang: str) -> Namespace:
    """Returns inference configuration based on the language."""
    return Namespace(
        model=MODELS_FOR_LANGUAGES[lang], 
        lang_id=lang,
        prior=f"config/languages/{lang}/prior.txt",
        device_id=-1,
        approximate=False
    )


def infer_phones(wav_file: str, lang: str) -> List[str]:
    """Performs phone inference using the recognizer model."""
    inference_config = get_inference_config(lang)
    
    recognizer = read_recognizer(inference_config_or_name=inference_config)
    return str(recognizer.recognize(wav_file, lang_id=lang)).split(" ")

def load_phoneme_mapping(lang: str) -> Dict[str, str]:
    """Loads phoneme mapping for a given language from a JSON file."""
    with open(f'config/languages/{lang}/phone_to_phonemes.json', 'r') as f:
        return cast(Dict[str, str], json.load(f))

def infer_phonemes(wav_file: str, lang: str) -> List[str]:
    """Performs phoneme inference."""
    phones = infer_phones(wav_file, lang)
    phonemes = load_phoneme_mapping(lang)
    return [phonemes.get(phone, "<unknown>") for phone in phones]