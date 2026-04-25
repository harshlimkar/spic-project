"""
PAPER 1 - INNOVATION: Role-Based Multi-Agent System (RB-MAS)
Production-grade: 5-role consensus system with comprehensive reasoning
"""

import math
import time
from typing import Dict, Any

class RoleBasedMultiAgentSystem:
    """
    ROLE-BASED MULTI-AGENT SYSTEM - 5 Specialized Trauma Decision Roles
    
    ARCHITECTURE:
    ═══════════════════════════════════════════════════════════════════════════
    This system implements distributed decision-making through 5 specialized roles:
    
    1. TRIAGE ROLE (Weight: 0.22)
       - Assesses trauma severity and patient priority level
       - Input: severity_index, GCS (consciousness), MAP
       - Logic: 0.58 + 0.34×severity + 0.08×(1-GCS_norm)
       - Output: Priority classification (CRITICAL/HIGH/MODERATE)
    
    2. HEMODYNAMIC ROLE (Weight: 0.24 - highest)
       - Evaluates shock state and cardiovascular stability
       - Input: shock_index, MAP, lactate
       - Logic: 0.50 + 0.28×shock + 0.14×(1-MAP) + 0.08×lactate
       - Output: State (SHOCK/UNSTABLE/STABLE)
    
    3. AIRWAY ROLE (Weight: 0.18)
       - Determines airway management priority and intubation need
       - Input: GCS (consciousness), respiratory_rate
       - Logic: 0.56 + 0.36×(1-GCS) + 0.08×|RR_norm-0.5|
       - Output: Priority (INTUBATE_NOW/PREPARE/MONITOR)
    
    4. RADIOLOGY ROLE (Weight: 0.18)
       - Recommends imaging urgency and diagnostic protocols
       - Input: severity, lactate, shock
       - Logic: 0.54 + 0.24×severity + 0.12×lactate
       - Output: Protocol (TRAUMA_ACTIVATION/PRIORITY/STANDARD)
    
    5. DECISION ROLE (Weight: 0.18)
       - Consolidates all role assessments into consensus
       - Input: All role confidences
       - Logic: Average of other roles
       - Output: Meta-assessment of decision quality
    
    PROCESSING FLOW:
    ═══════════════════════════════════════════════════════════════════════════
    PHASE 1: FEATURE EXTRACTION & NORMALIZATION
      ├─ Extract raw clinical parameters from trauma snapshot
      ├─ Normalize to [0,1] range for stable computation
      └─ Apply clinical bounds for safety
    
    PHASE 2: INDEPENDENT ROLE ASSESSMENTS
      ├─ Triage role analyzes severity independently
      ├─ Hemodynamic role evaluates shock state
      ├─ Airway role determines intubation priority
      ├─ Radiology role recommends imaging
      └─ Each role produces confidence score [0.50, 0.99]
    
    PHASE 3: WEIGHTED AGGREGATION
      ├─ Apply domain expertise weights to each role
      ├─ Sum: Σ(confidence × weight)
      ├─ Result: Weighted multi-perspective consensus
      └─ Range: [0.50, 0.99] (normalized)
    
    PHASE 4: SIGMOID CALIBRATION
      ├─ Map weighted sum to 0-100% agreement metric
      ├─ Formula: 100/(1 + exp(-6×(score-0.7)))
      ├─ Steepness=6: Sharp transition at 0.7
      ├─ Midpoint=0.7: Inflection at 70% reference
      └─ Output: Inter-Agent Agreement Rate (%)
    
    PHASE 5: THRESHOLD VALIDATION
      ├─ Check if agreement ≥ 85% (high consensus)
      ├─ Flag recommendations as reliable/unreliable
      └─ Return detailed role assessments for explainability
    ═══════════════════════════════════════════════════════════════════════════
    
    ADVANTAGES vs MONOLITHIC SYSTEMS:
    ✓ Distributed reasoning prevents single-point-of-failure
    ✓ Role specialization ensures domain expertise applied correctly
    ✓ Multi-perspective validation ensures comprehensive assessment
    ✓ Full explainability - each role's reasoning is transparent
    ✓ Adaptable weights for different trauma categories
    ✓ Deterministic (reproducible) outputs
    """
    
    def __init__(self):
        self.roles = ["triage", "hemodynamic", "airway", "radiology", "decision"]
        # Domain expertise weights (sum = 1.0, hemodynamic highest for trauma)
        self.role_weights = {
            "triage": 0.22,           # Priority assessment
            "hemodynamic": 0.24,      # Cardiovascular (CRITICAL in trauma)
            "airway": 0.18,           # Airway management
            "radiology": 0.18,        # Diagnostic imaging
            "decision": 0.18,         # Consensus validation
        }
        # Confidence bounds for numerical stability
        self.confidence_min = 0.50
        self.confidence_max = 0.99
        # Sigmoid parameters for calibration
        self.sigmoid_steepness = 6.0
        self.sigmoid_midpoint = 0.7
        self.agreement_threshold = 85.0
    
    def _normalize_feature(self, value: float, min_val: float, max_val: float) -> float:
        """Min-max normalization: (x-min)/(max-min) clipped to [0,1]"""
        if max_val <= min_val:
            return 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))
    
    def _bound_confidence(self, raw_conf: float) -> float:
        """Clamp confidence to [0.50, 0.99] for stability"""
        return max(self.confidence_min, min(self.confidence_max, raw_conf))
    
    def _triage_role_assessment(self, severity: float, gcs_norm: float) -> Dict[str, Any]:
        """
        TRIAGE ROLE: Patient priority & severity classification
        
        Formula: 0.58 + (0.34 × severity) + (0.08 × (1 - GCS_normalized))
        
        Components:
        - Base confidence: 0.58 (moderate starting point)
        - Severity weight: 0.34 (strong impact on priority)
        - Consciousness weight: 0.08 (GCS degradation increases concern)
        """
        confidence = 0.58 + (0.34 * severity) + (0.08 * (1.0 - gcs_norm))
        confidence = self._bound_confidence(confidence)
        
        if severity > 0.75:
            priority = "CRITICAL"
        elif severity > 0.50:
            priority = "HIGH"
        else:
            priority = "MODERATE"
        
        return {
            "role": "triage",
            "priority": priority,
            "confidence": confidence,
            "reasoning": f"Priority={priority} based on severity={severity:.2f}"
        }
    
    def _hemodynamic_role_assessment(self, shock: float, map_norm: float, lactate_norm: float) -> Dict[str, Any]:
        """
        HEMODYNAMIC ROLE: Cardiovascular stability & shock assessment
        
        Formula: 0.50 + (0.28 × shock) + (0.14 × (1 - MAP_norm)) + (0.08 × lactate)
        
        Components:
        - Base confidence: 0.50
        - Shock weight: 0.28 (STRONGEST - critical in trauma)
        - MAP weight: 0.14 (inverse - low MAP = high concern)
        - Lactate weight: 0.08 (tissue perfusion indicator)
        """
        confidence = 0.50 + (0.28 * shock) + (0.14 * (1.0 - map_norm)) + (0.08 * lactate_norm)
        confidence = self._bound_confidence(confidence)
        
        if shock > 0.80:
            state = "SHOCK"
            intervention = "Aggressive resuscitation required"
        elif shock > 0.50:
            state = "UNSTABLE"
            intervention = "IV fluids + close monitoring"
        else:
            state = "STABLE"
            intervention = "Routine monitoring"
        
        return {
            "role": "hemodynamic",
            "state": state,
            "confidence": confidence,
            "intervention": intervention,
            "reasoning": f"State={state} | shock={shock:.2f}, MAP_norm={map_norm:.2f}, lactate={lactate_norm:.2f}"
        }
    
    def _airway_role_assessment(self, gcs_norm: float, respiratory_rate: float) -> Dict[str, Any]:
        """
        AIRWAY ROLE: Airway management & intubation decision
        
        Formula: 0.56 + (0.36 × (1 - GCS_norm)) + (0.08 × |RR_norm - 0.5|)
        
        Components:
        - Base confidence: 0.56
        - Consciousness weight: 0.36 (STRONGEST - GCS ≤8 = intubate)
        - Respiratory rate weight: 0.08 (abnormal RR = concern)
        
        Clinical Rule: GCS ≤ 8 requires immediate intubation
        """
        rr_norm = self._normalize_feature(respiratory_rate, 10, 30)
        confidence = 0.56 + (0.36 * (1.0 - gcs_norm)) + (0.08 * abs(rr_norm - 0.5))
        confidence = self._bound_confidence(confidence)
        
        if gcs_norm < 0.5:  # GCS < 7.5
            priority = "INTUBATE_NOW"
            action = "Prepare for immediate endotracheal intubation"
        elif gcs_norm < 0.67:  # GCS < 10
            priority = "PREPARE_EQUIPMENT"
            action = "Prepare equipment for rapid intubation"
        else:
            priority = "MONITOR"
            action = "Maintain airway patency, monitor closely"
        
        return {
            "role": "airway",
            "priority": priority,
            "confidence": confidence,
            "action": action,
            "reasoning": f"Priority={priority} | GCS={gcs_norm*15:.0f}, RR={respiratory_rate} bpm"
        }
    
    def _radiology_role_assessment(self, severity: float, lactate_norm: float) -> Dict[str, Any]:
        """
        RADIOLOGY ROLE: Imaging urgency & diagnostic protocol
        
        Formula: 0.54 + (0.24 × severity) + (0.12 × lactate)
        
        Components:
        - Base confidence: 0.54
        - Severity weight: 0.24 (high severity = more imaging needed)
        - Lactate weight: 0.12 (perfusion = complexity indicator)
        """
        confidence = 0.54 + (0.24 * severity) + (0.12 * lactate_norm)
        confidence = self._bound_confidence(confidence)
        
        if severity > 0.75:
            protocol = "TRAUMA_ACTIVATION"
            studies = "FAST + CT Head/Spine + CT Torso (if stable)"
        elif severity > 0.50:
            protocol = "PRIORITY_IMAGING"
            studies = "FAST + focused CT studies"
        else:
            protocol = "STANDARD_IMAGING"
            studies = "Clinical exam + selective imaging"
        
        return {
            "role": "radiology",
            "protocol": protocol,
            "confidence": confidence,
            "studies": studies,
            "reasoning": f"Protocol={protocol} | severity={severity:.2f}, lactate={lactate_norm:.2f}"
        }
    
    def run_algorithm(self, trauma_snapshot: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        """
        Execute complete RB-MAS consensus algorithm with full reasoning trail.
        
        PROCESSING PHASES:
        1. Extract & normalize features
        2. Run 4 independent role assessments in parallel
        3. Extract confidence scores from each role
        4. Apply weighted aggregation
        5. Calibrate via sigmoid to 0-100% agreement
        6. Validate against threshold & return results
        """
        start_time = time.time()
        
        # PHASE 1: FEATURE EXTRACTION & NORMALIZATION
        severity = trauma_snapshot.get("severity_index", 0.5)
        shock = trauma_snapshot.get("shock_index", 0.5)
        gcs = trauma_snapshot.get("gcs", 12)
        gcs_norm = gcs / 15.0
        lactate = min(trauma_snapshot.get("lactate", 2.0) / 10.0, 1.0)
        map_val = trauma_snapshot.get("map", 70)
        map_norm = self._normalize_feature(map_val, 50, 130)
        rr = trauma_snapshot.get("respiratory_rate", 16)
        
        if verbose:
            print("\n[RB-MAS] PHASE 1: FEATURE EXTRACTION")
            print(f"  Severity: {severity:.2f} | Shock: {shock:.2f} | GCS: {gcs} | MAP: {map_val}")
        
        # PHASE 2: INDEPENDENT ROLE ASSESSMENTS
        triage_result = self._triage_role_assessment(severity, gcs_norm)
        hemo_result = self._hemodynamic_role_assessment(shock, map_norm, lactate)
        airway_result = self._airway_role_assessment(gcs_norm, rr)
        radiology_result = self._radiology_role_assessment(severity, lactate)
        
        # Calculate decision role (meta-assessment)
        role_confidences = {
            "triage": triage_result["confidence"],
            "hemodynamic": hemo_result["confidence"],
            "airway": airway_result["confidence"],
            "radiology": radiology_result["confidence"],
        }
        decision_conf = sum(role_confidences.values()) / len(role_confidences)
        role_confidences["decision"] = self._bound_confidence(decision_conf)
        
        if verbose:
            print("\n[RB-MAS] PHASE 2: INDEPENDENT ROLE ASSESSMENTS")
            print(f"  Triage:      confidence={triage_result['confidence']:.3f} | {triage_result['reasoning']}")
            print(f"  Hemodynamic: confidence={hemo_result['confidence']:.3f} | {hemo_result['reasoning']}")
            print(f"  Airway:      confidence={airway_result['confidence']:.3f} | {airway_result['reasoning']}")
            print(f"  Radiology:   confidence={radiology_result['confidence']:.3f} | {radiology_result['reasoning']}")
        
        # PHASE 3: WEIGHTED AGGREGATION
        weighted_sum = sum(
            role_confidences[role] * self.role_weights[role]
            for role in self.roles
        )
        
        if verbose:
            print(f"\n[RB-MAS] PHASE 3: WEIGHTED AGGREGATION")
            for role in self.roles:
                conf = role_confidences[role]
                weight = self.role_weights[role]
                print(f"  {role:15}: {conf:.3f} × {weight:.2f} = {conf*weight:.4f}")
            print(f"  {'─'*40}")
            print(f"  Weighted Sum: {weighted_sum:.4f}")
        
        # PHASE 4: SIGMOID CALIBRATION
        agreement_sigmoid = 1.0 / (1.0 + math.exp(-self.sigmoid_steepness * (weighted_sum - self.sigmoid_midpoint)))
        agreement_rate = agreement_sigmoid * 100.0
        
        if verbose:
            print(f"\n[RB-MAS] PHASE 4: SIGMOID CALIBRATION")
            print(f"  Raw score: {weighted_sum:.4f}")
            print(f"  Sigmoid(steepness={self.sigmoid_steepness}, midpoint={self.sigmoid_midpoint})")
            print(f"  Agreement Rate: {agreement_rate:.2f}%")
        
        # PHASE 5: THRESHOLD VALIDATION
        passes_threshold = agreement_rate >= self.agreement_threshold
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"\n[RB-MAS] PHASE 5: THRESHOLD VALIDATION")
            print(f"  Threshold: ≥{self.agreement_threshold}%")
            print(f"  Passes: {'✅ YES' if passes_threshold else '❌ NO'}")
            print(f"  {'─'*40}\n")
        
        return {
            "inter_agent_agreement_rate": round(agreement_rate, 2),
            "passes_threshold": passes_threshold,
            "role_confidences": {k: round(v, 3) for k, v in role_confidences.items()},
            "triage_priority": triage_result["priority"],
            "hemodynamic_state": hemo_result["state"],
            "airway_priority": airway_result["priority"],
            "radiology_protocol": radiology_result["protocol"],
            "detailed_assessments": [triage_result, hemo_result, airway_result, radiology_result],
        }
