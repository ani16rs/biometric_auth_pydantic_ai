from biometric_auth_pydantic_ai.router import router_agent, choose_modality
from biometric_auth_pydantic_ai.models import BiometricTemplate, BiometricSample
from biometric_auth_pydantic_ai.router import choose_modality
from biometric_auth_pydantic_ai.factory import run_authentication

instr_list = [
    "Scan my face. Let me in. ",
    "I want to log in using my voice",
    "I want to log in using my fingerprint",
    "I want to log in using my iris",
    "I want to log in using my password",
    ]

def run_demo():
    # Step 1: Natural language instruction
    for instruction in instr_list:
        result = choose_modality(instruction)
        print("Router decided modality:", result.output.modality)

    # # Step 2: Dummy enrollment template + sample
    # template = BiometricTemplate(
    #     user_id="alice",
    #     modality=modality,
    #     features=[0.12, 0.34, 0.56]
    # )

    # sample = BiometricSample(
    #     modality=modality,
    #     raw_data="base64_face_image_here"
    # )

    # # Step 3: Run authentication
    # result = run_authentication(template, sample)
    # print("Authentication result:", result.data)


if __name__ == "__main__":
    run_demo()
