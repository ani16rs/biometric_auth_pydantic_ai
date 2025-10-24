from biometric_auth_pydantic_ai.controller import controller_agent
from biometric_auth_pydantic_ai.executors import (
    InputManager,
    FeatureExtractor,
    TemplateManager,
    Matcher,
)
from biometric_auth_pydantic_ai.services import choose_modality, plan_pipeline
from biometric_auth_pydantic_ai.utils import clean_up_result
import json

instr_list = [
    "Compare my speech. Let me in ",
    "Scan my face. Let me in. ",
    "I want to log in using my fingerprint",
    "I want to log in using my iris",
    "I want to log in using my password",
]

def run_demo_no_controller():
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

def run_demo_controller():
    instruction = "I want to log in using my password"
    print(f"User instruction: {instruction}")
    print("\n[Controller Agent Running]")

    try:
        result = controller_agent.run_sync(instruction)
        print("\n[Controller Output]")

        raw_output = clean_up_result(result.output)
        controller_data = json.loads(raw_output)

        print("\nAgent decided modality:", controller_data["modality"])
        print("Planned steps:")
        for i, step in enumerate(controller_data["steps"], start=1):
            print(f"{i}. {step['agent']} - {step['step']}")

    except Exception as e:
        print("[Controller Error]", e)
        print("Gemini returned no final message — try rerunning or adjust system prompt.")


if __name__ == "__main__":
    # run_demo()
    run_demo_controller()
