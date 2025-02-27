import tempfile
import re
from noisereduce import reduce_noise
from pedalboard import Compressor, Gain, LowShelfFilter, NoiseGate, Pedalboard
from pedalboard.io import AudioFile
from pydub import AudioSegment
from typing import Dict, Tuple, Optional
import os

ml_models: Dict[str, None] = {}

def create_wav_file(audio_bytes: bytes, persist: bool = False) -> str:
    """Creates a WAV file from given audio bytes. If persist=True, stores it in a known directory."""
    if persist:
        save_dir = "saved_audio"
        os.makedirs(save_dir, exist_ok=True)
        temp_wav_path = os.path.join(save_dir, next(tempfile._get_candidate_names()) + ".wav")
    else:
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_wav_path = temp_wav.name
    
    with open(temp_wav_path, "wb") as wav_file:
        wav_file.write(audio_bytes)

    return temp_wav_path

def trim_audio(wav_file: str, attempt_word: str) -> None:
    result = ml_models["whisper"].transcribe(
        wav_file,
        word_timestamps=True
    )

    print(result)
    
    start_time, end_time = None, None
    
    if "segments" in result and result["segments"]:
        if "words" in result["segments"][0]:
            for word in result["segments"][0]["words"]:
                if re.sub(r'[\s\W_]+', '', word["word"]).lower() == attempt_word:
                    start_time = word["start"]
                    end_time = word["end"]
                    break
    


    if start_time is not None and end_time is not None:
        buffer = 250
        audio = AudioSegment.from_wav(wav_file)

        audio_length = len(audio)
        safe_start = max(0, start_time * 1000 - buffer)
        safe_end = min(audio_length, end_time * 1000 + buffer)
        trimmed_audio = audio[safe_start:safe_end]
        trimmed_audio.export(wav_file, format="wav")
        print("trimmed")

    print(start_time, end_time)
        
# def process_audio(wav_file: str, timing: Tuple[int, int]) -> None:
#     """Reads a WAV file, reduces noise, and returns processed audio data."""
#     sr = 44100
#     with AudioFile(wav_file).resampled_to(sr) as f:
#         audio = f.read(f.frames)
#         num_channels = audio.shape[1] if len(audio.shape) > 1 else 1

#     start_sample = int((timing[0] / 1000) * sr)
#     end_sample = int((timing[1] / 1000) * sr)
    
#     # Make sure we're not going out of bounds
#     end_sample = min(end_sample, audio.shape[0])
#     start_sample = max(0, start_sample)

#     # Properly slice based on dimensionality
#     if len(audio.shape) > 1:
#         trimmed_audio = audio[start_sample:end_sample, :]
#     else:
#         trimmed_audio = audio[start_sample:end_sample]

#     reduced_trimmed_audio = reduce_noise(y=trimmed_audio, sr=sr, stationary=True, prop_decrease=0.8)

#     board = Pedalboard([
#         NoiseGate(threshold_db=-20, ratio=2, release_ms=250),
#         Compressor(threshold_db=-12, ratio=4),
#         LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
#         Gain(gain_db=2)
#     ])
#     effected = board(reduced_trimmed_audio, sr)
    
#     # Make sure the processed audio has the correct shape
#     # If mono, reshape to 1D array
#     if num_channels == 1 and len(effected.shape) > 1:
#         effected = effected.mean(axis=1)  # Convert to mono if needed
    
#     # Write with proper number of channels
#     with AudioFile(wav_file, 'w', sr, num_channels=num_channels) as f:
#         f.write(effected)

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