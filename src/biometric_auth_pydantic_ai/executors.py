"""
    File name: executors.py

    Purpose:
        Local deterministic agents that perform actual biometric 
        operations for the POC.
"""

import hashlib
import random
import math
from biometric_auth_pydantic_ai.types import (
    BiometricTemplate,
    BiometricSample,
    MatchResult,
)

class InputManager:
    """
    Responsible for capturing or loading the raw input data.
    Each modality uses its own private helper method.
    """

    def capture_input(self, modality: str, path: str | None = None) -> BiometricSample:
        print(f"[InputManager] Capturing input for modality: {modality}")

        if modality == "password":
            return self._capture_password(path)
        elif modality == "voice":
            return self._capture_voice(path)
        elif modality == "face":
            return self._capture_face(path)
        else:
            data = f"mock_{modality}_input"
            print(f"[InputManager] Using mock input for unsupported modality: {modality}")
            return BiometricSample(modality=modality, raw_data=data)

    # Modality-specific helpers
    def _capture_password(self, path: str | None = None) -> BiometricSample:
        if path:
            with open(path, "r") as f:
                data = f.read().strip()
            print(f"[InputManager] Loaded password from file: {path}")
        else:
            # data = "my_secure_password"
            data = str(input("Enter password: "))           # mock password input
            print("[InputManager] Using mock password input.")
        
        return BiometricSample(modality="password", raw_data=data)

    def _capture_voice(self, path: str | None = None) -> BiometricSample:
        # todo: load audio or mock it
        print("[InputManager] Using mock voice input (placeholder).")
        return BiometricSample(modality="voice", raw_data="mock_voice_audio")

    def _capture_face(self, path: str | None = None) -> BiometricSample:
        # todo: load image or mock it
        print("[InputManager] Using mock face input (placeholder).")
        return BiometricSample(modality="face", raw_data="mock_face_image")

class TemplateManager:
    """
    Responsible for storing or retrieving enrolled (template) biometric data.
    """

    def fetch_template(self, user_id: str, modality: str) -> BiometricTemplate:
        print(f"[TemplateManager] Fetching template for user '{user_id}' ({modality})...")

        if modality == "password":
            return self._template_password(user_id)
        elif modality == "voice":
            return self._template_voice(user_id)
        elif modality == "face":
            return self._template_face(user_id)
        else:
            print(f"[TemplateManager] Using mock template for unsupported modality: {modality}")
            features = [random.random() for _ in range(4)]
            return BiometricTemplate(user_id=user_id, modality=modality, features=features)

    # Modality-specific templates
    def _template_password(self, user_id: str) -> BiometricTemplate:
        stored_hash = hashlib.sha256("my_secure_password".encode()).hexdigest()
        features = [int(stored_hash[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
        return BiometricTemplate(user_id=user_id, modality="password", features=features)

    def _template_voice(self, user_id: str) -> BiometricTemplate:
        features = [0.15, 0.22, 0.31, 0.44]
        return BiometricTemplate(user_id=user_id, modality="voice", features=features)

    def _template_face(self, user_id: str) -> BiometricTemplate:
        features = [0.11, 0.28, 0.39, 0.47]
        return BiometricTemplate(user_id=user_id, modality="face", features=features)

class FeatureExtractor:
    """
    Converts raw input into comparable numeric features.
    Each modality has its own extraction logic.
    """

    def extract(self, sample: BiometricSample) -> list[float]:
        print(f"[FeatureExtractor] Extracting features from {sample.modality} input...")

        if sample.modality == "password":
            return self._extract_password(sample.raw_data)
        elif sample.modality == "voice":
            return self._extract_voice(sample.raw_data)
        elif sample.modality == "face":
            return self._extract_face(sample.raw_data)
        else:
            print(f"[FeatureExtractor] Using mock feature vector for unsupported modality: {sample.modality}")
            return [random.random() for _ in range(4)]

    # Modality-specific extraction
    def _extract_password(self, raw_data: str) -> list[float]:
        hashed = hashlib.sha256(raw_data.encode()).hexdigest()
        features = [int(hashed[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
        return features

    def _extract_voice(self, raw_data: str) -> list[float]:
        # todo: voice feature extraction
        return [random.random() for _ in range(4)]

    def _extract_face(self, raw_data: str) -> list[float]:
        # todo: face embedding
        return [random.random() for _ in range(4)]


class Matcher:
    """
    Compares extracted features with the stored template and returns a similarity score.
    """

    def compare(self, template: BiometricTemplate, features: list[float]) -> MatchResult:
        print(f"[Matcher] Comparing features for modality '{template.modality}'...")

        dot = sum(t * s for t, s in zip(template.features, features))
        norm_t = math.sqrt(sum(t * t for t in template.features))
        norm_s = math.sqrt(sum(s * s for s in features))
        score = dot / (norm_t * norm_s + 1e-8)

        if template.modality == "password":
            threshold = 0.95
        else:
            threshold = 0.8

        match = score > threshold

        print(f"[Matcher] Similarity score: {score:.3f}")
        print(f"[Matcher] Match decision: {'MATCH' if match else 'NO MATCH'}")

        return MatchResult(match=match, score=round(score, 3))