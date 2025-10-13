from biometric_auth_pydantic_ai.services import choose_modality, plan_pipeline

instr_list = [
    "Compare my speech. Let me in ",
    "Scan my face. Let me in. ",
    "I want to log in using my fingerprint",
    "I want to log in using my iris",
    "I want to log in using my password",
]

def run_demo():
    # Step 1: Natural language instruction
    instruction = instr_list[2]
    modality_choice = choose_modality(instruction)
    print("Agent decided modality:", modality_choice.modality)

    # Step 2: Decide what is needed
    plan = plan_pipeline(modality_choice.modality)
    print("Pipeline steps and agents:")
    for i, step in enumerate(plan.steps, start=1):
        print(f"{i}. Agent: {step.agent} - {step.step} ")

    print("-" * 40)

    print(f"First to call: {plan.steps[0].agent}")

    # Step 3: Create agents
    # InputManager      finds input file
    # TemplateManager   finds template file
    # FeatureExtractor  performs FE from input
    # Matcher           compares Finput with Ftemplate
    
if __name__ == "__main__":
    run_demo()
