import tempfile

from noisereduce import reduce_noise
from pedalboard.io import AudioFile
from pedalboard import *

def create_wav_file(audio_bytes: bytes) -> str:
    """Creates a temporary WAV file from given audio bytes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        return temp_wav.name

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