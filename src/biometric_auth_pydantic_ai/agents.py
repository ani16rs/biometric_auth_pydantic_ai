import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from .models import MatchResult

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))

def make_voice_matcher():
    return Agent(
        model=GoogleModel("gemini-1.5-flash", provider=provider),
        result_type=MatchResult,
        system_prompt="You are a voice matcher. Compare template vs sample and return {match: bool, score: float}."
    )

def make_face_matcher():
    return Agent(
        model=GoogleModel("gemini-1.5-flash", provider=provider),
        result_type=MatchResult,
        system_prompt="You are a face matcher. Compare template vs sample and return {match: bool, score: float}."
    )
