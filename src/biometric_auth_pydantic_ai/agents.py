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
        "Valid options: voice, face, fingerprint, iris, password."
        "Always respond with JSON: {modality: string}."
    ),
)

planner_agent = Agent(
    model=model,
    output_type=PipelinePlan,
    system_prompt=(
        "You are a biometric authenticator pipeline planner.\n"
        "Input: a modality (e.g., face, voice, fingerprint, iris, password).\n"
        "Output: a JSON object with {steps: [{step: string, agent: string}]}.\n"
        "Tell what steps are required to compare an input sample to a stored template.\n\n"
        "Each step should briefly describe what to do, and specify which agent is responsible.\n\n"
        "Agents available: InputManager, TemplateManager, FeatureExtractor, Matcher.\n"
        "Always return 3–6 steps, short and clear."
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
