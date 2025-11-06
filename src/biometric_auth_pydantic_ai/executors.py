"""
    File name: executors.py

    Purpose:
        Local deterministic agents that perform actual biometric 
        operations for the POC.
"""

from biometric_auth_pydantic_ai.types import (
    BiometricTemplate,
    BiometricSample,
    MatchResult,
)
from dotenv import load_dotenv
import hashlib
import math
import os
import random
import nbis
from nbis import NbisExtractor, NbisExtractorSettings

load_dotenv()
PASSWORD_THRESHOLD = 1
FINGERPRINT_THRESHOLD = 50

# Configuration for the NbisExtractor
extractor_settings = NbisExtractorSettings(
    min_quality=0.0,                    # Do not filter on minutiae quality (get all minutiae)
    get_center=False,                   # Do not get the fingerprint center or ROI
    check_fingerprint=False,            # Do not use SIVV to check if the image is a fingerprint
    compute_nfiq2=False,                # Do not compute the NFIQ2 quality score
    ppi=None,                           # No specific PPI, use the default
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
        elif modality == "fingerprint":
            return self._capture_fingerprint(path)
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
            data = str(input("[InputManager] Enter password: "))        # my_secure_password
        return BiometricSample(modality="password", raw_data=data)

    def _capture_fingerprint(self, path: str | None = None) -> BiometricSample:
        image_bytes = open(path, "rb").read()                           # Read the bytes from a file
        return BiometricSample(modality="fingerprint", raw_data=image_bytes)


class TemplateManager:
    """
    Responsible for storing or retrieving enrolled (template) biometric data.
    """

    def fetch_template(self, user_id: str, modality: str, path: str) -> BiometricTemplate:
        print(f"[TemplateManager] Fetching template for user '{user_id}' ({modality})...")

        if modality == "password":
            return self._template_password(user_id)
        elif modality == "fingerprint":
            return self._template_fingerprint(user_id, path)
        else:
            print(f"[TemplateManager] Using mock template for unsupported modality: {modality}")
            features = [random.random() for _ in range(4)]
            return BiometricTemplate(user_id=user_id, modality=modality, features=features)

    # Modality-specific templates
    def _template_password(self, user_id: str) -> BiometricTemplate:
        mock_password = os.getenv("MOCK_PASSWORD")
        stored_hash = hashlib.sha256(mock_password.encode()).hexdigest()
        features = [int(stored_hash[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
        return BiometricTemplate(user_id=user_id, modality="password", features=features)

    def _template_fingerprint(self, user_id: str, path: str) -> BiometricTemplate:
        image_bytes = open(path, "rb").read()       # Read the bytes from a file
        feature_extractor = nbis.new_nbis_extractor(extractor_settings)
        minutiae_obj = feature_extractor.extract_minutiae(image_bytes)
        return BiometricTemplate(user_id=user_id, modality="fingerprint", features=minutiae_obj)

class FeatureExtractor:
    """
    Converts raw input into comparable numeric features.
    Each modality has its own extraction logic.
    """

    def extract(self, sample: BiometricSample) -> list[float]:
        print(f"[FeatureExtractor] Extracting features from {sample.modality} input...")

        if sample.modality == "password":
            return self._extract_password(sample.raw_data)
        elif sample.modality == "fingerprint":
            return self._extract_fingerprint(sample.raw_data)
        else:
            print(f"[FeatureExtractor] Using mock feature vector for unsupported modality: {sample.modality}")
            return [random.random() for _ in range(4)]

    # Modality-specific extraction
    def _extract_password(self, raw_data: str) -> list[float]:
        hashed = hashlib.sha256(raw_data.encode()).hexdigest()
        features = [int(hashed[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
        return features

    def _extract_fingerprint(self, raw_data) -> list[float]:
        feature_extractor = nbis.new_nbis_extractor(extractor_settings)
        minutiae_obj = feature_extractor.extract_minutiae(raw_data)
        return minutiae_obj


class Matcher:
    """
    Compares extracted features with the stored template and returns a similarity score.
    """

    def compare(self, modality: str, template: BiometricTemplate, sample_features) -> MatchResult:
        print(f"[Matcher] Comparing features for modality '{template.modality}'...")
        if modality == "password":
            return self._compare_password(template, sample_features)
        elif modality == "fingerprint":
            return self._compare_fingerprint(template, sample_features)
        else:
            print(f"[FeatureExtractor] Using mock feature vector for unsupported modality: {modality}")
            return [random.random() for _ in range(4)]

    def _compare_password(self, template: BiometricTemplate, features: list[float]):
        dot = sum(t * s for t, s in zip(template.features, features))
        norm_t = math.sqrt(sum(t * t for t in template.features))
        norm_s = math.sqrt(sum(s * s for s in features))
        score = dot / (norm_t * norm_s + 1e-8)

        match = score > PASSWORD_THRESHOLD

        print(f"[Matcher] Similarity score: {score:.3f}")
        print(f"[Matcher] Match decision: {'MATCH' if match else 'NO MATCH'}")

        return MatchResult(match=match, score=round(score, 3))

    def _compare_fingerprint(self, template: BiometricTemplate, features):
        score = template.features.compare(features)
        match = score > FINGERPRINT_THRESHOLD
        return MatchResult(match=match, score=round(score, 3))