from .agents import make_voice_matcher, make_face_matcher
from .models import BiometricTemplate, BiometricSample

def get_matcher(modality: str):
    if modality == "voice":
        return make_voice_matcher()
    elif modality == "face":
        return make_face_matcher()
    else:
        raise ValueError(f"Unsupported modality: {modality}")

def run_authentication(template: BiometricTemplate, sample: BiometricSample):
    matcher = get_matcher(template.modality)
    return matcher.run(
        f"Compare template: {template.features} with sample data: {sample.raw_data}"
    )
