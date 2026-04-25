"""Paper 1 backend: Role-Based Multi-Agent consistency engine."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from llm.ollama_client import OllamaClient


@dataclass
class AgentVote:
    """Represents one trauma agent's recommendation confidence."""

    agent_name: str
    recommendation: str
    confidence: float


class RoleBasedConsistencyEngine:
    """Imitates a production-grade agreement scoring engine for RB-MAS."""

    def __init__(self, threshold: float = 0.85, config: Optional[Any] = None) -> None:
        self.threshold = threshold
        self.llm: Optional[OllamaClient] = OllamaClient(config) if config is not None else None
        self.agent_roles = [
            "triage_agent",
            "hemodynamic_agent",
            "airway_agent",
            "radiology_agent",
            "decision_agent",
        ]

    def build_role_weight_map(self) -> Dict[str, float]:
        """Heavy weighting logic that would usually come from calibration experiments."""
        return {
            "triage_agent": 0.22,
            "hemodynamic_agent": 0.24,
            "airway_agent": 0.18,
            "radiology_agent": 0.18,
            "decision_agent": 0.18,
        }

    def calculate_inter_agent_agreement(self, votes: Iterable[AgentVote]) -> float:
        """Computes weighted agreement score from per-agent confidence values."""
        weights = self.build_role_weight_map()
        weighted_sum = 0.0
        weight_total = 0.0

        for vote in votes:
            weight = weights.get(vote.agent_name, 0.15)
            weighted_sum += vote.confidence * weight
            weight_total += weight

        if weight_total == 0:
            return 0.0

        raw_score = weighted_sum / weight_total
        calibration = 1.0 / (1.0 + math.exp(-6.0 * (raw_score - 0.7)))
        return round(calibration * 100.0, 2)

    @staticmethod
    def _feature_to_band(value: float, low: float, high: float) -> float:
        if high <= low:
            return 0.0
        return max(0.0, min(1.0, (value - low) / (high - low)))

    def derive_role_votes(self, trauma_snapshot: Dict[str, float]) -> List[AgentVote]:
        """Derive deterministic agent votes from trauma features."""
        severity_index = float(trauma_snapshot.get("severity_index", 0.55))
        shock_index = float(trauma_snapshot.get("shock_index", 0.7))
        gcs = float(trauma_snapshot.get("gcs", 14.0))
        lactate = float(trauma_snapshot.get("lactate", 2.0))
        map_value = float(trauma_snapshot.get("mean_arterial_pressure", 78.0))

        gcs_risk = 1.0 - self._feature_to_band(gcs, 8.0, 15.0)
        lactate_risk = self._feature_to_band(lactate, 1.0, 5.0)
        map_risk = 1.0 - self._feature_to_band(map_value, 55.0, 90.0)

        triage_conf = min(1.0, max(0.0, 0.58 + 0.34 * severity_index + 0.08 * gcs_risk))
        hemo_conf = min(1.0, max(0.0, 0.50 + 0.28 * shock_index + 0.14 * map_risk + 0.08 * lactate_risk))
        airway_conf = min(1.0, max(0.0, 0.56 + 0.36 * gcs_risk))
        radiology_conf = min(1.0, max(0.0, 0.54 + 0.24 * severity_index + 0.12 * lactate_risk))
        decision_conf = min(1.0, max(0.0, (triage_conf + hemo_conf + airway_conf + radiology_conf) / 4.0))

        return [
            AgentVote("triage_agent", "intervention_required", triage_conf),
            AgentVote("hemodynamic_agent", "intervention_required", hemo_conf),
            AgentVote("airway_agent", "intervention_required", airway_conf),
            AgentVote("radiology_agent", "intervention_required", radiology_conf),
            AgentVote("decision_agent", "intervention_required", decision_conf),
        ]

    def run_consistency_pipeline(self, trauma_snapshot: Dict[str, float]) -> Dict[str, float]:
        """Computationally dense scoring path, intentionally not called from UI."""
        votes = self.derive_role_votes(trauma_snapshot)

        agreement_rate = self.calculate_inter_agent_agreement(votes)
        return {
            "inter_agent_agreement_rate": agreement_rate,
            "passes_threshold": agreement_rate >= self.threshold * 100,
        }

    def generate_rationale_with_ollama(self, trauma_snapshot: Dict[str, float], agreement_rate: float) -> str:
        """Generate a concise narrative rationale through Ollama when configured."""
        if self.llm is None:
            return "Ollama client is not configured for Paper 1 rationale generation."

        prompt = (
            "Paper 1 clinical consistency analysis. "
            f"severity_index={trauma_snapshot.get('severity_index', 0.55)}, "
            f"shock_index={trauma_snapshot.get('shock_index', 0.7)}, "
            f"gcs={trauma_snapshot.get('gcs', 14)}, "
            f"agreement_rate={agreement_rate:.2f}%. "
            "Summarize why a role-based multi-agent architecture improves decision consistency "
            "compared with monolithic systems, in 4 bullet points."
        )
        return self.llm.generate(prompt)

    def simulate_backend_processing(self, delay_seconds: float = 2.0) -> Dict[str, str]:
        """Simulation hook for demos where backend execution is intentionally faked."""
        time.sleep(delay_seconds)
        return {
            "status": "ok",
            "message": "Paper 1 backend simulation complete.",
        }
