import asyncio
import json
import logging
import os
import uuid
import warnings
from typing import Dict, List, Optional

import whisper
from gtts import gTTS
from pydub import AudioSegment

from app.services.audio_processing import ml_models
from app.services.inference import infer_word_and_phonemes


# Suppress UserWarnings from Whisper
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('evaluation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
WORDS = [
    "knife", "psychology", "debt", "pneumonia", "queue", "beautiful", "business",
    "strength", "sixth", "breadth", "isthmus", "clothes", "colonel", "comfortable",
    "mischievous", "february", "wednesday", "specifically", "compiler", "hardware",
    "software", "keyboard", "mouse", "computer", "parrot"
]
OUTPUT_JSON_FILE = "evaluation_results.json"

class AudioGenerationError(Exception):
    """Custom exception for audio generation errors."""
    pass

def generate_pronunciation_wav(word: str) -> str:
    try:
        # Generate temporary filename
        temp_mp3_filename = f"{uuid.uuid4()}.mp3"
        temp_wav_filename = f"{uuid.uuid4()}.wav"

        # Generate TTS audio
        tts = gTTS(text=word, lang='en')
        tts.save(temp_mp3_filename)

        # Convert MP3 to WAV
        audio = AudioSegment.from_mp3(temp_mp3_filename)
        audio.export(temp_wav_filename, format="wav")

        # Remove temporary MP3
        os.remove(temp_mp3_filename)

        logger.info(f"Successfully generated audio for {word}")
        return temp_wav_filename

    except Exception as e:
        logger.error(f"Failed to generate audio for {word}: {e}")
        raise AudioGenerationError(f"Could not generate audio for {word}")

async def evaluate_word(word: str) -> Optional[List[str]]:
    try:
        logger.info(f"Processing word: {word}")
        
        audio_file = generate_pronunciation_wav(word)
        
        model_response = infer_word_and_phonemes(audio_file, "eng")

        if model_response.success:
            logger.info(f"Inferred phonemes for '{word}': {model_response.phonemes}")
        else:
            logger.warning(f"Failed to infer phonemes for '{word}'")
        
        os.remove(audio_file)
        
        return model_response.phonemes

    except AudioGenerationError:
        logger.error(f"Could not generate audio for {word}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing {word}: {e}")
        return None
    
async def evaluate_model() -> None:
    results: Dict[str, List[str]] = {}  # Dictionary to store phonemes for each word

    for word in WORDS:
        result = await evaluate_word(word)
        if result is not None:
            results[word] = result

    # Write results to JSON file
    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)

async def main() -> None:
    """Main async entry point."""
    try:
        logger.info("Loading Whisper model...")
        ml_models["whisper"] = whisper.load_model("tiny.en")
        await evaluate_model()
        ml_models.clear()
    except Exception as e:
        logger.error(f"Critical error in main process: {e}")
    finally:
        logger.info("Evaluations complete.")

if __name__ == "__main__":
    asyncio.run(main())