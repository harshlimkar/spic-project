"""
PAPER 4 - COMPARISON: Black-Box AI Systems
Baseline system without explainability - lower trust
"""

import time

class BlackBoxAISystem:
    """
    Black-box AI system provides predictions without explanation.
    Results in lower clinician trust and limited human control.
    """
    
    def __init__(self):
        self.name = "Black-Box AI"
    
    def run_algorithm(self, trauma_case, verbose=True):
        """
        Execute black-box baseline algorithm.
        
        Args:
            trauma_case: Dict with case features
            verbose: Print progress
            
        Returns:
            Dict with clinician_trust_score_percent (lower baseline)
        """
        start_time = time.time()
        
        if verbose:
            print("[Black-Box AI] Starting baseline trust assessment...")
        
        # Black-box systems have inherently lower trust due to lack of explainability
        base_trust = 0.50  # Lower baseline trust
        
        # Minor improvement with experience but fundamentally limited
        experience_factor = trauma_case.get("system_experience_months", 6) / 100
        guideline_match = trauma_case.get("guideline_match", 0.8)
        
        # Trust score calculation without explainability boost
        trust_raw = base_trust + (experience_factor * 0.1) + (guideline_match * 0.15)
        trust_score = min(0.85, max(0.45, trust_raw)) * 100
        
        if verbose:
            print(f"  [Base Trust] {base_trust:.3f}")
            print(f"  [Experience Factor] {experience_factor:.3f}")
            print(f"  [Trust Score] {trust_score:.2f}%")
        
        elapsed = time.time() - start_time
        
        return {
            "clinician_trust_score_percent": round(trust_score, 2),
            "trust_band": "moderate" if trust_score >= 60 else "low",
            "execution_time": elapsed,
        }
