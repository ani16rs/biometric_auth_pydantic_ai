from pydantic import BaseModel

class BiometricTemplate(BaseModel):
    user_id: str
    modality: str   # "voice", "face", etc.
    features: list[float]

class BiometricSample(BaseModel):
    modality: str
    raw_data: str   # base64, filepath, etc.

class MatchResult(BaseModel):
    match: bool
    score: float

class ModalityChoice(BaseModel):
    modality: str   # e.g. "voice", "face", "fingerprint", "iris", "password"
