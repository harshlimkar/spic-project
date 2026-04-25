"""Paper 3 backend: Verification-driven safety guard for recommendations."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from llm.ollama_client import OllamaClient


class VerificationSafetyGuardian:
    """Imitates multi-layer verification to estimate unsafe recommendation rate."""

    def __init__(self, config: Optional[Any] = None) -> None:
        self.llm: Optional[OllamaClient] = OllamaClient(config) if config is not None else None
        self.validation_layers = [
            "contraindication_scan",
            "dose_sanity_check",
            "temporal_consistency_check",
            "protocol_alignment_check",
            "risk_escalation_review",
        ]
        self.layer_weights = {
            "contraindication_scan": 0.24,
            "dose_sanity_check": 0.21,
            "temporal_consistency_check": 0.17,
            "protocol_alignment_check": 0.19,
            "risk_escalation_review": 0.19,
        }

    @staticmethod
    def _feature_to_band(value: float, low: float, high: float) -> float:
        if high <= low:
            return 0.0
        return max(0.0, min(1.0, (value - low) / (high - low)))

    def build_risk_vector(self, trauma_case: Dict[str, float]) -> List[float]:
        """Heavy synthetic risk-vector computation for verification stages."""
        severity = float(trauma_case.get("severity_index", 0.55))
        comorbidity_load = float(trauma_case.get("comorbidity_load", 0.40))
        polypharmacy_index = float(trauma_case.get("polypharmacy_index", 0.35))
        renal_risk = float(trauma_case.get("renal_risk", 0.25))

        vector: List[float] = []
        for layer in self.validation_layers:
            layer_weight = self.layer_weights[layer]
            base = 0.008 + (severity * 0.020)

            if layer == "contraindication_scan":
                adjusted = base + (polypharmacy_index * 0.030) + (comorbidity_load * 0.012)
            elif layer == "dose_sanity_check":
                adjusted = base + (renal_risk * 0.032) + (severity * 0.010)
            elif layer == "temporal_consistency_check":
                adjusted = base + (severity * 0.018)
            elif layer == "protocol_alignment_check":
                adjusted = base + (comorbidity_load * 0.020)
            else:
                adjusted = base + (severity * 0.015) + (comorbidity_load * 0.012)

            weighted = adjusted * (0.85 + layer_weight)
            vector.append(max(0.005, min(0.20, weighted)))

        return vector

    def verify_recommendation_path(self, trauma_case: Dict[str, float]) -> Dict[str, float]:
        """Aggregates layer risks into unsafe recommendation rate."""
        vector = self.build_risk_vector(trauma_case)
        unsafe_rate = (sum(vector) / len(vector)) * 100.0 if vector else 0.0

        return {
            "unsafe_recommendation_rate_percent": round(unsafe_rate, 2),
            "is_safe": unsafe_rate < 5.0,
        }

    def generate_rationale_with_ollama(self, trauma_case: Dict[str, float], unsafe_rate: float) -> str:
        """Generate a concise safety-layer rationale through Ollama when configured."""
        if self.llm is None:
            return "Ollama client is not configured for Paper 3 rationale generation."

        prompt = (
            "Paper 3 verification-driven safety analysis. "
            f"severity_index={trauma_case.get('severity_index', 0.55)}, "
            f"comorbidity_load={trauma_case.get('comorbidity_load', 0.40)}, "
            f"polypharmacy_index={trauma_case.get('polypharmacy_index', 0.35)}, "
            f"unsafe_rate={unsafe_rate:.2f}%. "
            "Explain how multi-layer verification reduces unsafe trauma recommendations "
            "versus direct-prediction AI, in 4 bullet points."
        )
        return self.llm.generate(prompt)

    def simulate_backend_processing(self, delay_seconds: float = 2.0) -> Dict[str, str]:
        """Simulation hook for demos where backend execution is intentionally faked."""
        time.sleep(delay_seconds)
        return {
            "status": "ok",
            "message": "Paper 3 backend simulation complete.",
        }
