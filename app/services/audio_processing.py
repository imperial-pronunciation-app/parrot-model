import tempfile

from noisereduce import reduce_noise
from scipy.io import wavfile


def create_wav_file(audio_bytes: bytes) -> str:
    """Creates a temporary WAV file from given audio bytes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        return temp_wav.name

def process_audio(wav_file: str) -> None:
    """Reads a WAV file, reduces noise, and returns processed audio data."""
    rate, data = wavfile.read(wav_file)

    # Handle mono vs stereo
    if len(data.shape) == 1:
        nchannels, nframes = 1, len(data)
        data = data.reshape(1, -1)
    else:
        nframes, nchannels = data.shape

    # Noise reduction
    reduced_data = reduce_noise(y=data.reshape(nchannels, nframes), sr=rate)

    # Save the processed file
    wavfile.write(wav_file, rate, reduced_data.reshape(nframes, nchannels))