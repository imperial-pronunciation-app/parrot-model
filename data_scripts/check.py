import json
from typing import Dict, List

from allosaurus.app import Namespace, read_recognizer


# need to download the eng2102 model inside the container

# !python -m allosaurus.bin.download_model -m eng2102
inference_config = Namespace(model="eng2102", lang_id="eng", prior="prior.txt", device_id=-1, approximate=False)
recognizer = read_recognizer(inference_config_or_name=inference_config)
words = ["hello", "software", "hardware", "mountain", "parrot", "computer"]
# Load the phoneme mapping from phoible_2178.json
with open('resources/phoible_2176.json', 'r') as f:
  phoneme_mapping = json.load(f)




def map_phones_to_phonemes(phones: List[str], mapping: Dict[str, str]) -> List[str]:
  phonemes = []
  for phone in phones:
    phoneme = mapping.get(phone, phone)  # Use the phone itself if no mapping is found
    phonemes.append(phoneme)
  return phonemes

for word in words:
  result = recognizer.recognize(f"samples/{word}.wav", lang_id="eng")
  print(f"Word: {word}")
  print(f"Phones: {result}")
  phones = result.split(" ")
  print(f"Phonemes: {map_phones_to_phonemes(phones, phoneme_mapping)}")
  