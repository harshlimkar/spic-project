"""Paper 2 backend: HTD multi-agent timing and accuracy engine."""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from llm.ollama_client import OllamaClient


@dataclass
class TaskExecutionUnit:
    """Represents one HTD sub-task with execution timing and confidence."""

    task_name: str
    duration_seconds: float
    confidence: float


class HTDDecisionLatencyEngine:
    """Simulates a structured planner for decision-time and accuracy analysis."""

    def __init__(self, config: Optional[Any] = None) -> None:
        self.llm: Optional[OllamaClient] = OllamaClient(config) if config is not None else None
        self.task_graph = [
            "stabilize_airway",
            "evaluate_hemodynamics",
            "order_imaging",
            "crosscheck_drug_contraindications",
            "select_intervention_path",
        ]
        self.task_base_duration = {
            "stabilize_airway": 1.35,
            "evaluate_hemodynamics": 1.55,
            "order_imaging": 1.20,
            "crosscheck_drug_contraindications": 1.05,
            "select_intervention_path": 1.30,
        }
        self.task_base_confidence = {
            "stabilize_airway": 0.94,
            "evaluate_hemodynamics": 0.93,
            "order_imaging": 0.92,
            "crosscheck_drug_contraindications": 0.95,
            "select_intervention_path": 0.93,
        }

    @staticmethod
    def _feature_to_band(value: float, low: float, high: float) -> float:
        if high <= low:
            return 0.0
        return max(0.0, min(1.0, (value - low) / (high - low)))

    def decompose_case_into_tasks(self, trauma_case: Dict[str, float]) -> List[TaskExecutionUnit]:
        """Builds a weighted HTD plan and execution profile."""
        base_complexity = float(trauma_case.get("complexity", 0.58))
        vitals_instability = float(trauma_case.get("vitals_instability", 0.42))
        comorbidity_load = float(trauma_case.get("comorbidity_load", 0.36))
        case_pressure = (0.45 * base_complexity) + (0.35 * vitals_instability) + (0.20 * comorbidity_load)

        complexity_modifier = 1.0 + self._feature_to_band(case_pressure, 0.15, 0.95) * 0.55
        confidence_penalty = self._feature_to_band(case_pressure, 0.2, 0.95) * 0.09

        units: List[TaskExecutionUnit] = []

        for idx, task in enumerate(self.task_graph, start=1):
            base_duration = self.task_base_duration[task]
            coordination_bonus = 0.05 * (idx - 1)
            duration = max(0.75, base_duration * complexity_modifier - coordination_bonus)

            base_confidence = self.task_base_confidence[task]
            depth_bonus = 0.006 * idx
            confidence = min(0.99, max(0.78, base_confidence - confidence_penalty + depth_bonus))

            units.append(TaskExecutionUnit(task_name=task, duration_seconds=duration, confidence=confidence))

        return units

    def evaluate_decision_profile(self, units: Iterable[TaskExecutionUnit]) -> Dict[str, float]:
        """Aggregates latency and quality into a final profile."""
        unit_list = list(units)
        total_time = sum(unit.duration_seconds for unit in unit_list)
        mean_confidence = statistics.mean(unit.confidence for unit in unit_list) if unit_list else 0.0

        return {
            "decision_time_seconds": round(total_time, 2),
            "accuracy_rate_percent": round(mean_confidence * 100.0, 2),
        }

    def run_htd_pipeline(self, trauma_case: Dict[str, float]) -> Dict[str, float]:
        """Dense pipeline entry point for production-like orchestration."""
        units = self.decompose_case_into_tasks(trauma_case)
        return self.evaluate_decision_profile(units)

    def generate_rationale_with_ollama(self, trauma_case: Dict[str, float], profile: Dict[str, float]) -> str:
        """Generate a concise HTD rationale through Ollama when configured."""
        if self.llm is None:
            return "Ollama client is not configured for Paper 2 rationale generation."

        prompt = (
            "Paper 2 trauma HTD analysis. "
            f"complexity={trauma_case.get('complexity', 0.58)}, "
            f"vitals_instability={trauma_case.get('vitals_instability', 0.42)}, "
            f"decision_time={profile.get('decision_time_seconds', 0.0)}s, "
            f"accuracy={profile.get('accuracy_rate_percent', 0.0)}%. "
            "Explain how hierarchical task decomposition reduces decision latency "
            "while preserving clinical accuracy, in 4 bullet points."
        )
        return self.llm.generate(prompt)

    def simulate_backend_processing(self, delay_seconds: float = 2.0) -> Dict[str, str]:
        """Simulation hook for demos where backend execution is intentionally faked."""
        time.sleep(delay_seconds)
        return {
            "status": "ok",
            "message": "Paper 2 backend simulation complete.",
        }
