"""
    File name: controller.py

    Purpose:
        Handler functions for agents.
"""

from .agents import modality_agent, planner_agent
from .types import ModalityChoice, PipelinePlan

def choose_modality(instruction: str) -> ModalityChoice:
    """
    Decide the authentication modality from a natural-language instruction.
    """
    # using run_sync so that nothing else runs while LLM decides modality
    result = modality_agent.run_sync(instruction)   # todo: change run_sync to run if needed
    return result.output

def plan_pipeline(modality: str) -> PipelinePlan:
    """Generate a numbered list of steps for the given modality"""
    result = planner_agent.run_sync(f"Plan pipeline for {modality} authentication")
    return result.output
