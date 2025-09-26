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



# def get_matcher(modality: str):
#     if modality == "voice":
#         return make_voice_matcher()
#     elif modality == "face":
#         return make_face_matcher()
#     else:
#         raise ValueError(f"Unsupported modality: {modality}")

# def run_authentication(template: BiometricTemplate, sample: BiometricSample):
#     matcher = get_matcher(template.modality)
#     return matcher.run(
#         f"Compare template: {template.features} with sample data: {sample.raw_data}"
#     )
