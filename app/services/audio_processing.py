import re
import tempfile
from typing import Dict

from noisereduce import reduce_noise
from pedalboard import Compressor, Gain, LowShelfFilter, NoiseGate, Pedalboard
from pedalboard.io import AudioFile
from pydub import AudioSegment


ml_models: Dict[str, None] = {}
BUFFER_MS = 250
SAMPLE_RATE = 44100

def create_wav_file(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        return temp_wav.name

def trim_audio(wav_file: str, attempt_word: str) -> bool:
    """Trims the audio file to the start and end times of the attempt word.
    Returns True if the word was found and trimmed, False otherwise.
    """
    
    result = ml_models["whisper"].transcribe( # type: ignore
        wav_file,
        word_timestamps=True
    )
    
    start_time, end_time = None, None

    if "segments" in result and result["segments"]:
        if "words" in result["segments"][0]:
            for word in result["segments"][0]["words"]:
                if re.sub(r'[\s\W_]+', '', word["word"]).lower() == attempt_word:
                    start_time = word["start"]
                    end_time = word["end"]
                    audio = AudioSegment.from_wav(wav_file)

                    safe_start = max(0, start_time * 1000 - BUFFER_MS)
                    safe_end = min(len(audio), end_time * 1000 + BUFFER_MS)
                    trimmed_audio = audio[safe_start:safe_end]
                    trimmed_audio.export(wav_file, format="wav")
                    return True
    return False

def process_audio(wav_file: str) -> None:
    """Reads a WAV file, reduces noise, and returns processed audio data."""
    with AudioFile(wav_file).resampled_to(SAMPLE_RATE) as f:
        audio = f.read(f.frames)
    reduced_noise = reduce_noise(y=audio, sr=SAMPLE_RATE, stationary=True, prop_decrease=0.8)
    board = Pedalboard([
        NoiseGate(threshold_db=-20, ratio=2, release_ms=250),
        Compressor(threshold_db=-12, ratio=4),
        LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
        Gain(gain_db=2)
    ])
    effected = board(reduced_noise, SAMPLE_RATE)
    with AudioFile(wav_file, 'w', SAMPLE_RATE, effected.shape[0]) as f:
        f.write(effected)