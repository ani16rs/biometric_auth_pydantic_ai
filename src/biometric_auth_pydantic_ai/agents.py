from dotenv import load_dotenv
import os
from .types import PipelinePlan, ModalityChoice

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv()

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)

modality_agent = Agent(
    model=model,
    output_type=ModalityChoice,
    system_prompt=(
        "You are a biometric authentication modality selector. "
        "Given a user's natural-language request "
        "(e.g., 'I want to log in using my face'), "
        "decide the intended modality. "
        "Valid options: voice, face, fingerprint, iris, password. "
        "Always respond with JSON: {modality: string}."
    ),
)

planner_agent = Agent(
    model=model,
    output_type=PipelinePlan,
    system_prompt=(
        "You are a biometric pipeline planner."
        "Input: a modality (e.g., face, voice, fingerprint, iris, password). "
        "Output: a brief, numbered list of concrete authentication steps. "
        "Tell what steps are required to compare an input sample to a stored template."
        "Be concise, 3–6 steps. Tailor steps to the modality "
        "(e.g., liveness checks for face, noise handling for voice). "
        "Each step should be short and clear."
        "Return JSON as {steps: string[]}."
    )
)



# def make_voice_matcher():
#     return Agent(
#         model=GoogleModel("gemini-1.5-flash", provider=provider),
#         result_type=MatchResult,
#         system_prompt="You are a voice matcher. Compare template vs sample and return {match: bool, score: float}."
#     )

# def make_face_matcher():
#     return Agent(
#         model=GoogleModel("gemini-1.5-flash", provider=provider),
#         result_type=MatchResult,
#         system_prompt="You are a face matcher. Compare template vs sample and return {match: bool, score: float}."
#     )
