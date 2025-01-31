from typing import List

from pydantic import BaseModel


# No request for now, it's just a wav file
# Could potentially include language in the future

class InferPhonemesResponse(BaseModel):
    phonemes: List[str]