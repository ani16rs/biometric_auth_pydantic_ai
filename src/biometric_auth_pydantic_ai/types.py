"""
    File name: types.py

    Purpose:
        Data types for biometric auth system.
"""

from pydantic import BaseModel
from typing import List

class ModalityChoice(BaseModel):
    modality: str   # "voice", "face", "fingerprint", "iris", "password"

class PipelineStep(BaseModel):
    step: str
    agent: str

class PipelinePlan(BaseModel):
    steps: List[PipelineStep]

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
