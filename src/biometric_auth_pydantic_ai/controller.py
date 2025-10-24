"""
controller.py
--------------
An agentic orchestrator that autonomously decides which LLM tools to call.
It can call the modality selector and pipeline planner tools in sequence,
making the system agent-driven rather than manual.
"""

import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from biometric_auth_pydantic_ai.services import choose_modality, plan_pipeline
from biometric_auth_pydantic_ai.types import ModalityChoice, PipelinePlan

# Load environment variables
load_dotenv()
provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))
model = GoogleModel("gemini-2.5-flash", provider=provider)

controller_agent = Agent(
    model=model,
    system_prompt=(
        "You are a controller agent for a biometric authentication system.\n"
        "Valid options: voice, face, fingerprint, iris, password."
        "Your job is to decide the modality from a user's instruction and then "
        "generate a biometric pipeline plan for that modality.\n"
        "For this purpose, use the following tools:\n"
        "- choose_modality(instruction: str) → returns ModalityChoice\n"
        "- plan_pipeline(modality: str) → returns PipelinePlan\n"
        "After calling these tools, always respond in structured JSON as:\n"
        "{modality: string, steps: [{step: string, agent: string}]}.\n"
        "Each step must include both the action (step) and responsible agent name."
    ),
)

@controller_agent.tool
def choose_modality_tool(ctx: RunContext) -> ModalityChoice:
    """Decide the authentication modality from a user's natural instruction."""
    print("     [choose_modality_tool] running")
    return choose_modality(ctx.prompt)

@controller_agent.tool
def plan_pipeline_tool(ctx: RunContext, modality: str) -> PipelinePlan:
    """Generate a numbered list of steps for the given modality."""
    print("     [plan_pipeline_tool] running")
    return plan_pipeline(modality)

