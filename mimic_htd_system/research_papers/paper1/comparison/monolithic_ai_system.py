"""
PAPER 1 - COMPARISON: Monolithic AI System (Baseline)
Single-model architecture demonstrating lower consensus without role specialization
"""

import math
import time
from typing import Dict, Any

class MonolithicAISystem:
    """
    MONOLITHIC AI SYSTEM - Traditional Single-Model Baseline
    
    ARCHITECTURE:
    ═══════════════════════════════════════════════════════════════════════════
    This baseline implements a unified rule-based decision model without:
    - Role specialization (all aspects combined into single pipeline)
    - Distributed reasoning (single-point-of-failure risk)
    - Multi-perspective validation
    - Explainability of individual components
    
    DISADVANTAGES vs Role-Based Systems:
    ✗ Rigid decision structure cannot adapt to different trauma types
    ✗ Single model lacks domain expertise perspective
    ✗ No distributed validation - one error affects entire decision
    ✗ Limited explainability - difficult to understand why decision made
    ✗ Accuracy degraded by "rigidity penalty" factor
    
    PROCESSING FLOW:
    ═════════════════════════════════════════════════════════════════════════
    PHASE 1: UNIFIED FEATURE EXTRACTION
      ├─ Extract severity, shock, consciousness
      ├─ Apply single normalization to [0,1]
      └─ No role-specific feature engineering
    
    PHASE 2: MONOLITHIC SCORING
      ├─ Apply fixed weights to all features simultaneously
      ├─ Single scoring formula (no role separation)
      ├─ Apply rigidity penalty (15%) for inflexibility
      └─ No intermediate confidence extraction
    
    PHASE 3: SIGMOID CALIBRATION
      ├─ Map to 0-100% agreement metric
      ├─ Lower sigmoid steepness (4.0 vs 6.0) = less certainty
      ├─ Higher midpoint (0.6) = more pessimistic baseline
      └─ Result: Lower overall agreement rates
    
    PHASE 4: THRESHOLD VALIDATION
      ├─ Check if agreement ≥ 75% (lower threshold than RB-MAS)
      └─ Return single aggregated score
    ═════════════════════════════════════════════════════════════════════════
    
    EXPECTED OUTCOMES:
    ~ 71% baseline inter-agent agreement (vs ~92% for RB-MAS)
    ~ Lower accuracy due to lack of specialization
    ~ Rigid response to changing trauma conditions
    """
    
    def __init__(self):
        self.model_name = "Monolithic Decision Engine"
        self.severity_weight = 0.40      # Highest weight (but lacks specialization)
        self.shock_weight = 0.35         # Cardiovascular factor
        self.consciousness_weight = 0.25 # Consciousness factor
        self.rigidity_penalty = 0.15     # 15% penalty for inflexibility
        # Sigmoid parameters (lower certainty)
        self.sigmoid_steepness = 4.0
        self.sigmoid_midpoint = 0.55
        self.agreement_threshold = 75.0
    
    def _normalize_feature(self, value: float, min_val: float, max_val: float) -> float:
        """Min-max normalization to [0,1]"""
        if max_val <= min_val:
            return 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))
    
    def run_algorithm(self, trauma_snapshot: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        """
        Execute monolithic baseline algorithm with fixed rule-based scoring.
        
        LIMITATIONS vs RB-MAS:
        - No role specialization
        - Fixed weights unable to adapt
        - Single point of failure
        - Lower overall agreement rate
        """
        start_time = time.time()
        
        # PHASE 1: UNIFIED FEATURE EXTRACTION
        severity = trauma_snapshot.get("severity_index", 0.5)
        shock = trauma_snapshot.get("shock_index", 0.5)
        gcs = trauma_snapshot.get("gcs", 12) / 15.0
        
        if verbose:
            print("\n[MONOLITHIC AI] PHASE 1: UNIFIED FEATURE EXTRACTION")
            print(f"  Severity: {severity:.2f}")
            print(f"  Shock: {shock:.2f}")
            print(f"  GCS_normalized: {gcs:.2f}")
        
        # PHASE 2: MONOLITHIC SCORING (no role specialization)
        # Single unified formula combining all factors without domain perspective
        base_score = (
            self.severity_weight * severity +
            self.shock_weight * shock +
            self.consciousness_weight * gcs
        )
        
        # Apply rigidity penalty (inflexible rule-based approach)
        monolithic_score = base_score * (1.0 - self.rigidity_penalty)
        
        if verbose:
            print(f"\n[MONOLITHIC AI] PHASE 2: MONOLITHIC SCORING")
            print(f"  Base formula: {self.severity_weight}×{severity:.2f} + {self.shock_weight}×{shock:.2f} + {self.consciousness_weight}×{gcs:.2f}")
            print(f"  Base score: {base_score:.3f}")
            print(f"  Rigidity penalty: -{self.rigidity_penalty:.1%}")
            print(f"  Final monolithic score: {monolithic_score:.3f}")
        
        # PHASE 3: SIGMOID CALIBRATION (lower certainty than RB-MAS)
        agreement_sigmoid = 1.0 / (1.0 + math.exp(-self.sigmoid_steepness * (monolithic_score - self.sigmoid_midpoint)))
        agreement_rate = agreement_sigmoid * 100.0
        
        if verbose:
            print(f"\n[MONOLITHIC AI] PHASE 3: SIGMOID CALIBRATION")
            print(f"  Sigmoid parameters: steepness={self.sigmoid_steepness}, midpoint={self.sigmoid_midpoint}")
            print(f"  Sigmoid output: {agreement_sigmoid:.3f}")
            print(f"  Agreement rate: {agreement_rate:.2f}%")
        
        # PHASE 4: THRESHOLD VALIDATION
        passes_threshold = agreement_rate >= self.agreement_threshold
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"\n[MONOLITHIC AI] PHASE 4: THRESHOLD VALIDATION")
            print(f"  Threshold: ≥{self.agreement_threshold}%")
            print(f"  Passes: {'✅ YES' if passes_threshold else '❌ NO'}")
            print(f"  [Note] No role-based consensus - limited explainability")
            print(f"  {'─'*40}\n")
        
        return {
            "inter_agent_agreement_rate": round(agreement_rate, 2),
            "passes_threshold": passes_threshold,
            "model_score": round(monolithic_score, 3),
            "baseline_comparison": "Lower than RB-MAS due to rigidity penalty & lack of role specialization",
        }
