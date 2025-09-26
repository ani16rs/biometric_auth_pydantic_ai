from dotenv import load_dotenv
import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from .models import ModalityChoice

load_dotenv()

provider = GoogleProvider(api_key=os.getenv("GEMINI_API_KEY"))

router_agent = Agent(
    model=GoogleModel("gemini-2.5-flash", provider=provider),
    output_type=ModalityChoice,
    system_prompt=(
        "You are a biometric authentication router. "
        "Given a user request, decide the authentication modality."
        "Valid options: voice, face, fingerprint, iris, password. "
        "Always respond with {modality: string}."
    ),
)

def choose_modality(instruction: str) -> ModalityChoice:
    """Run the router agent and return the chosen modality"""
    # using run_sync so that nothing else runs while LLM decides modality
    return router_agent.run_sync(instruction)       # todo: change run_sync to run if needed