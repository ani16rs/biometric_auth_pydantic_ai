"""
    File name: types.py

    Purpose:
        Data types for biometric auth system.
"""

from pydantic import BaseModel
from typing import List
from nbis.nbis import Minutiae

class PipelineStep(BaseModel):
    step: str
    agent: str

class PipelinePlan(BaseModel):
    steps: List[PipelineStep]

class BiometricTemplate(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    user_id: str
    modality: str
    features: List[float] | Minutiae

class BiometricSample(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    modality: str
    raw_data: str | bytes | Minutiae

class MatchResult(BaseModel):
    match: bool
    score: float
