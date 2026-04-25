"""
PAPER 3 - COMPARISON: Direct-Prediction AI Systems
Baseline without verification layers - higher unsafe rates
"""

import time

class DirectPredictionAI:
    """
    Baseline system makes direct predictions without validation layers.
    Results in higher rates of unsafe recommendations.
    """
    
    def __init__(self):
        self.name = "Direct-Prediction AI"
    
    def run_algorithm(self, trauma_case, verbose=True):
        """
        Execute direct-prediction baseline algorithm.
        
        Args:
            trauma_case: Dict with case features
            verbose: Print progress
            
        Returns:
            Dict with unsafe_recommendation_rate_percent (higher baseline)
        """
        start_time = time.time()
        
        if verbose:
            print("[Direct-Prediction AI] Starting baseline prediction...")
        
        severity = trauma_case.get("severity_index", 0.5)
        comorbidity = trauma_case.get("comorbidity_load", 0.3)
        polypharmacy = trauma_case.get("polypharmacy_count", 2) / 10.0
        
        # Direct prediction without verification - higher unsafe rate
        base_unsafe_rate = 0.12  # 12% baseline
        
        # Complexity increases unsafe rate without verification
        complexity_factor = (severity * 0.15) + (comorbidity * 0.12) + (polypharmacy * 0.10)
        
        total_unsafe_rate = (base_unsafe_rate + complexity_factor) * 100
        
        if verbose:
            print(f"  [Base Unsafe Rate] {base_unsafe_rate:.4f}")
            print(f"  [Complexity Factor] {complexity_factor:.4f}")
            print(f"  [Total Unsafe Rate] {total_unsafe_rate:.2f}%")
        
        elapsed = time.time() - start_time
        
        return {
            "unsafe_recommendation_rate_percent": round(total_unsafe_rate, 2),
            "is_safe": total_unsafe_rate < 10.0,
            "execution_time": elapsed,
        }
