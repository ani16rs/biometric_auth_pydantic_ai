"""
    File name: controller.py

    Purpose:
        An agentic orchestrator that autonomously decides which LLM tools to call.
"""

import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from biometric_auth_pydantic_ai.executors import InputManager, FeatureExtractor, TemplateManager, Matcher
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from biometric_auth_pydantic_ai.services import choose_modality, plan_pipeline
from biometric_auth_pydantic_ai.types import (
    BiometricSample, 
    BiometricTemplate, 
    ModalityChoice, 
    PipelinePlan
)

# Load environment variables
load_dotenv()
provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)

controller_agent = Agent(
    model=model,
    system_prompt=(
        "You are the controller agent for a biometric authentication system.\n"
        "Valid biometric options: voice, face, fingerprint, iris, password."
        "Given a user's instruction, you must:\n"
        "1. Decide the modality using choose_modality(instruction)\n"
        "2. Generate a pipeline plan using plan_pipeline(modality)\n"
        "3. Execute the authentication steps by calling:\n"
        "   - capture_input_tool(modality)\n"
        "   - extract_features_tool(modality, raw_data)\n"
        "   - fetch_template_tool(user_id, modality)\n"
        "   - compare_features_tool(template_features, features, modality)\n"
        "Return the final result as structured JSON containing:\n"
        "{modality: string, steps: [{agent: string, step: string}], match: bool, score: float}.\n"
        "Include the same steps you planned and executed. Do not wrap the JSON in markdown fences."
    ),
)

@controller_agent.tool
def choose_modality_tool(ctx: RunContext) -> ModalityChoice:
    """
    Decide the authentication modality from a user's natural instruction.
    """
    print("     [choose_modality_tool] running")
    return choose_modality(ctx.prompt)

@controller_agent.tool
def plan_pipeline_tool(ctx: RunContext, modality: str) -> PipelinePlan:
    """
    Generate a numbered list of steps for the given modality.
    """
    print("     [plan_pipeline_tool] running")
    return plan_pipeline(modality)

@controller_agent.tool
def capture_input_tool(ctx: RunContext, modality: str) -> str:
    """
    Capture raw user input using the appropriate InputManager.
    """
    sample = InputManager().capture_input(modality)
    return sample.raw_data  # return raw data as string


@controller_agent.tool
def extract_features_tool(ctx: RunContext, modality: str, raw_data: str) -> list[float]:
    """
    Extract comparable features from raw input.
    """
    sample = BiometricSample(modality=modality, raw_data=raw_data)
    features = FeatureExtractor().extract(sample)
    return features

@controller_agent.tool
def fetch_template_tool(ctx: RunContext, user_id: str, modality: str) -> list[float]:
    """
    Fetch the enrolled template features for a given user.
    """
    template = TemplateManager().fetch_template(user_id, modality)
    return template.features

@controller_agent.tool
def compare_features_tool(ctx: RunContext, template_features: list[float], features: list[float], modality: str) -> dict:
    """
    Compare extracted features with stored template and return match result.
    """
    template = BiometricTemplate(user_id="alice", modality=modality, features=template_features)
    result = Matcher().compare(template, features)
    return {"match": result.match, "score": result.score}
