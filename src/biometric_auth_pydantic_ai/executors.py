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
            data = "my_secure_password"  # mock password input
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


