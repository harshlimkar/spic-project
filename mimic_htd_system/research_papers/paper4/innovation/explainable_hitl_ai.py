"""
PAPER 4 - INNOVATION: Explainable AI + Human-in-the-Loop (XAI+HITL)
Trust-building system with transparency and human control
"""

import math
import time

class ExplainableHITLAI:
    """
    Explainable AI system with human-in-the-loop control.
    Four explainability factors increase clinician trust.
    """
    
    def __init__(self):
        self.explainability_factors = {
            "traceability": 0.28,
            "counterfactual_support": 0.24,
            "guideline_alignment": 0.20,
            "human_override_visibility": 0.28,
        }
    
    def run_algorithm(self, trauma_case, verbose=True):
        """
        Execute XAI+HITL trust calibration algorithm.
        
        Args:
            trauma_case: Dict with case features
            verbose: Print progress
            
        Returns:
            Dict with clinician_trust_score_percent
        """
        start_time = time.time()
        
        if verbose:
            print("[XAI+HITL] Starting explainability-driven trust calculation...")
        
        # Explainability factors
        explanation_coverage = trauma_case.get("explanation_coverage", 0.7)
        guideline_match = trauma_case.get("guideline_match", 0.8)
        hitl_presence = trauma_case.get("hitl_presence", 0.85)
        auditability = trauma_case.get("auditability", 0.75)
        
        # Calculate four explainability dimensions
        traceability = 0.66 + 0.30 * explanation_coverage + 0.04 * auditability
        counterfactual = 0.62 + 0.28 * explanation_coverage + 0.06 * hitl_presence
        guideline = 0.64 + 0.32 * guideline_match + 0.03 * auditability
        human_override = 0.60 + 0.34 * hitl_presence + 0.04 * explanation_coverage
        
        factor_scores = {
            "traceability": min(1.0, max(0.5, traceability)),
            "counterfactual_support": min(1.0, max(0.5, counterfactual)),
            "guideline_alignment": min(1.0, max(0.5, guideline)),
            "human_override_visibility": min(1.0, max(0.5, human_override)),
        }
        
        if verbose:
            print("  [Explainability Factors]:")
            for factor, score in factor_scores.items():
                weight = self.explainability_factors[factor]
                print(f"    {factor}: {score:.3f} (weight={weight:.2f})")
        
        # Weighted trust calculation
        trust_raw = sum(factor_scores[factor] * self.explainability_factors[factor]
                       for factor in self.explainability_factors)
        
        # Sigmoid calibration for trust score
        trust_score = 100.0 / (1 + math.exp(-7 * (trust_raw - 0.48)))
        
        if verbose:
            print(f"  [Raw Trust Score] {trust_raw:.3f}")
            print(f"  [Calibrated Trust Score] {trust_score:.2f}%")
        
        elapsed = time.time() - start_time
        
        return {
            "clinician_trust_score_percent": round(trust_score, 2),
            "trust_band": "high" if trust_score >= 80 else "moderate",
            "execution_time": elapsed,
        }
