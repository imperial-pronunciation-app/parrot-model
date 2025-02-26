import tempfile

from noisereduce import reduce_noise
from pedalboard import Compressor, Gain, LowShelfFilter, NoiseGate, Pedalboard
from pedalboard.io import AudioFile
from typing import Dict

ml_models: Dict[str, None] = {}

def create_wav_file(audio_bytes: bytes) -> str:
    """Creates a temporary WAV file from given audio bytes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        return temp_wav.name

def detect_audio_start_time(wav_file: str, attempt_word: str) -> None:
    """Detects the start time of the user-pronounced audio in the given WAV file."""

    result = ml_models["whisper"].transcribe(wav_file, word_timestamps=True)  # Enable word-level timestamps)

    print(attempt_word)
    print(result)

def process_audio(wav_file: str) -> None:
    """Reads a WAV file, reduces noise, and returns processed audio data."""
    sr=44100
    with AudioFile(wav_file).resampled_to(sr) as f:
        audio = f.read(f.frames)
    reduced_noise = reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.8)
    board = Pedalboard([
        NoiseGate(threshold_db=-20, ratio=2, release_ms=250),
        Compressor(threshold_db=-12, ratio=4),
        LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
        Gain(gain_db=2)
    ])
    effected = board(reduced_noise, sr)
    with AudioFile(wav_file, 'w', sr, effected.shape[0]) as f:
        f.write(effected)