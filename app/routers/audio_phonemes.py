import json
import tempfile
from typing import Dict, List

from allosaurus.app import Namespace, read_recognizer
from fastapi import APIRouter, UploadFile
from noisereduce import reduce_noise
from scipy.io import wavfile

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        return temp_wav.name

@router.post("/api/v1/infer_phonemes", response_model = InferPhonemesResponse)
async def phonemes(audio_file: UploadFile) -> InferPhonemesResponse:
    # Read audio bytes from uploaded file
    audio_bytes = await audio_file.read()
    
    # Create temporary WAV file
    wav_file = create_wav_file(audio_bytes)
    
    # Read audio data from WAV file
    rate, data = wavfile.read(wav_file)
    
    # Handle mono vs. stereo data
    if len(data.shape) == 1:
        nchannels, nframes = 1, len(data)
        data = data.reshape(1, -1)
    else:
        nframes, nchannels = data.shape
    
    # Noise reduction
    reduced_data = reduce_noise(y=data.reshape(nchannels, nframes), sr=rate)
    
    # Save processed file back
    wavfile.write(wav_file, rate, reduced_data.reshape(nframes, nchannels))
    
    # Perform phoneme inference
    inference_config = Namespace(model="eng2102", lang_id="eng", prior="app/prior.txt", device_id=-1, approximate=False)
    recognizer = read_recognizer(inference_config_or_name=inference_config)
    result = recognizer.recognize(wav_file, lang_id="eng")
    
    # Convert recognized phones to phonemes
    phones = result.split(" ")
    with open('resources/phoible_2176.json', 'r') as f:
        phoneme_mapping = json.load(f)
    phonemes = map_phones_to_phonemes(phones, phoneme_mapping)
    
    return InferPhonemesResponse(phonemes = phonemes)

# for testing
@router.get("/api/v1/phones", response_model = InferPhonemesResponse)
async def get_phonemes() -> InferPhonemesResponse:
    return InferPhonemesResponse(phonemes = ["a", "b", "c"])