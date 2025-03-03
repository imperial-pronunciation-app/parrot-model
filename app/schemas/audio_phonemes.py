from typing import List

from pydantic import BaseModel


class InferPhonemesResponse(BaseModel):
    phonemes: List[str]
    success: bool # for clarity
