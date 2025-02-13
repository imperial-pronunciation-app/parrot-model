import json
from typing import Dict, List

from allosaurus.app import Namespace, read_recognizer
from fastapi import APIRouter, UploadFile
from noisereduce import reduce_noise
from scipy.io import wavfile
import numpy as np

from app.schemas.audio_phonemes import InferPhonemesResponse


router = APIRouter()
ml_models: Dict[str, None] = {}

def map_phones_to_phonemes(phones: List[str], mapping: Dict[str, str]) -> List[str]:
    phonemes = []   
    for phone in phones:
        phoneme = mapping.get(phone, "<unknown>")
        phonemes.append(phoneme)
    return phonemes

def create_wav_file(audio_bytes: bytes) -> str:
    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)
    return "audio.wav"

@router.post("/api/v1/infer_phonemes", response_model = InferPhonemesResponse)
async def phonemes(audio_file: UploadFile) -> InferPhonemesResponse:
    audio_bytes = await audio_file.read()
    wav_file = create_wav_file(audio_bytes)

    rate, data = wavfile.read(wav_file)
    nframes, nchannels = data.shape
    reduced_data = reduce_noise(y=data.reshape(nchannels, nframes), sr=rate)
    wavfile.write(wav_file, rate, reduced_data.reshape(nframes, nchannels))
    
    inference_config = Namespace(model="eng2102", lang_id="eng", prior="app/prior.txt", device_id=-1, approximate=False)
    recognizer = read_recognizer(inference_config_or_name=inference_config)
    
    result = recognizer.recognize(wav_file, lang_id="eng")
    phones = result.split(" ")
    with open('resources/phoible_2176.json', 'r') as f:
        phoneme_mapping = json.load(f)
    phonemes = map_phones_to_phonemes(phones, phoneme_mapping)
    
    return InferPhonemesResponse(phonemes = phonemes)

# for testing
@router.get("/api/v1/phones", response_model = InferPhonemesResponse)
async def get_phonemes() -> InferPhonemesResponse:
    return InferPhonemesResponse(phonemes = ["a", "b", "c"])