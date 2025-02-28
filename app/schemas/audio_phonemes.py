from typing import List, Optional

from pydantic import BaseModel


class InferPhonemesResponse(BaseModel):
    phonemes: Optional[List[str]]
    success: bool # for clarity
