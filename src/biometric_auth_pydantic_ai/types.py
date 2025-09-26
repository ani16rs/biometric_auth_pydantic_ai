from pydantic import BaseModel
from typing import List

class ModalityChoice(BaseModel):
    modality: str   # e.g. "voice", "face", "fingerprint", "iris", "password"

class PipelinePlan(BaseModel):
    steps: list[str]

class BiometricTemplate(BaseModel):
    user_id: str
    modality: str
    features: List[float]

class BiometricSample(BaseModel):
    modality: str
    raw_data: str

class MatchResult(BaseModel):
    match: bool
    score: float
