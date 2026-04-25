"""Paper 4 backend: Explainable HITL trust calibration engine."""

from __future__ import annotations

import math
import time
from typing import Any, Dict, Optional

from llm.ollama_client import OllamaClient


class ExplainableTrustCalibrationEngine:
    """Models explainability + HITL effects on clinician trust."""

    def __init__(self, config: Optional[Any] = None) -> None:
        self.llm: Optional[OllamaClient] = OllamaClient(config) if config is not None else None
        self.explanation_factors = {
            "traceability": 0.28,
            "counterfactual_support": 0.24,
            "guideline_alignment": 0.20,
            "human_override_visibility": 0.28,
        }

    @staticmethod
    def _feature_to_band(value: float, low: float, high: float) -> float:
        if high <= low:
            return 0.0
        return max(0.0, min(1.0, (value - low) / (high - low)))

    def calculate_trust_score(self, explainability_vector: Dict[str, float]) -> float:
        """Combines explainability dimensions into calibrated trust score."""
        weighted = 0.0
        for factor, weight in self.explanation_factors.items():
            weighted += explainability_vector.get(factor, 0.0) * weight

        normalized = max(0.0, min(1.0, weighted))
        calibrated = 1.0 / (1.0 + math.exp(-7.0 * (normalized - 0.48)))
        return round(calibrated * 100.0, 2)

    def run_trust_calibration(self, trauma_case: Dict[str, float]) -> Dict[str, float]:
        """Production-like trust calibration path, intentionally decoupled from UI."""
        explanation_coverage = float(trauma_case.get("explanation_coverage", 0.82))
        auditability = float(trauma_case.get("auditability", 0.78))
        hitl_presence = float(trauma_case.get("hitl_presence", 0.86))
        guideline_match = float(trauma_case.get("guideline_match", 0.84))

        explainability_vector = {
            "traceability": min(1.0, max(0.0, 0.66 + explanation_coverage * 0.30 + auditability * 0.04)),
            "counterfactual_support": min(1.0, max(0.0, 0.62 + explanation_coverage * 0.28 + hitl_presence * 0.06)),
            "guideline_alignment": min(1.0, max(0.0, 0.64 + guideline_match * 0.32 + auditability * 0.03)),
            "human_override_visibility": min(1.0, max(0.0, 0.60 + hitl_presence * 0.34 + explanation_coverage * 0.04)),
        }
        trust_score = self.calculate_trust_score(explainability_vector)

        return {
            "clinician_trust_score_percent": trust_score,
            "trust_band": "high" if trust_score >= 80 else "moderate",
        }

    def generate_rationale_with_ollama(self, trauma_case: Dict[str, float], trust_score: float) -> str:
        """Generate a concise trust rationale through Ollama when configured."""
        if self.llm is None:
            return "Ollama client is not configured for Paper 4 rationale generation."

        prompt = (
            "Paper 4 explainable HITL trust analysis. "
            f"explanation_coverage={trauma_case.get('explanation_coverage', 0.82)}, "
            f"auditability={trauma_case.get('auditability', 0.78)}, "
            f"hitl_presence={trauma_case.get('hitl_presence', 0.86)}, "
            f"guideline_match={trauma_case.get('guideline_match', 0.84)}, "
            f"trust_score={trust_score:.2f}. "
            "Explain why explainable human-in-the-loop architecture improves clinician trust "
            "versus black-box AI, in 4 bullet points."
        )
        return self.llm.generate(prompt)

    def simulate_backend_processing(self, delay_seconds: float = 2.0) -> Dict[str, str]:
        """Simulation hook for demos where backend execution is intentionally faked."""
        time.sleep(delay_seconds)
        return {
            "status": "ok",
            "message": "Paper 4 backend simulation complete.",
        }
