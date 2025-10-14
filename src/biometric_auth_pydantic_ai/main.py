from biometric_auth_pydantic_ai.services import choose_modality, plan_pipeline
from biometric_auth_pydantic_ai.executors import (
    InputManager,
    FeatureExtractor,
    TemplateManager,
    Matcher,
)

instr_list = [
    "Compare my speech. Let me in ",
    "Scan my face. Let me in. ",
    "I want to log in using my fingerprint",
    "I want to log in using my iris",
    "I want to log in using my password",
]

def run_demo():
    # Step 1: Natural language instruction
    instruction = instr_list[4]
    print(f"User instruction: {instruction}")
    modality_choice = choose_modality(instruction)
    print("\nAgent decided modality:", modality_choice.modality)

    # Step 2: Decide what is needed
    plan = plan_pipeline(modality_choice.modality)
    print("\nPipeline steps and agents:")
    for i, step in enumerate(plan.steps, start=1):
        print(f"{i}. Agent: {step.agent} - {step.step} ")

    print("-" * 50)
    print("\n[Executing Pipeline Locally]")

    # Step 3: Create agents
    input_mgr    = InputManager()
    extractor    = FeatureExtractor()
    template_mgr = TemplateManager()
    matcher      = Matcher()

    # Step 4: Run agents
    sample   = input_mgr.capture_input(modality_choice.modality)
    features = extractor.extract(sample)
    template = template_mgr.fetch_template(user_id="alice", modality=modality_choice.modality)
    result   = matcher.compare(template, features)

    # Step 5: Final result
    print("\n" + "-" * 50)
    print(f"Authentication Result:")
    print(f"Match: {result.match}, Score: {result.score}")
    print("-" * 50)
    
if __name__ == "__main__":
    run_demo()
