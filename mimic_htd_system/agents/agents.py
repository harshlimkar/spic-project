"""
Multi-Agent System with Hierarchical Task Decomposition (HTD)

Agents:
  1. ContextUnderstandingAgent  — interprets patient feature set
  2. AnalysisAgent— structured clinical reasoning
  3. ResourcePlanni              ngAgent      — determines action recommendations
  4. DecisionAgent              — aggregates + calls LLM for synthesis

Each agent operates independently, sharing only explicit output contracts.
"""

import logging
import json
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("Agents")


# ── Base Agent ────────────────────────────────────────────────────────────────

class BaseAgent:
    name: str = "BaseAgent"

    def __init__(self, config):
        self.config = config
        self.step_count = 0
        self.log: List[str] = []

    def _log(self, msg: str):
        entry = f"[{self.name}] {msg}"
        self.log.append(entry)
        logger.debug(entry)

    def run(self, inputs: Dict) -> Dict:
        raise NotImplementedError


# ── Agent 1: Context Understanding ───────────────────────────────────────────

class ContextUnderstandingAgent(BaseAgent):
    name = "ContextUnderstandingAgent"

    def run(self, inputs: Dict) -> Dict:
        self.step_count = 0
        case = inputs.get("case", {})
        self._log("Starting context understanding…")

        demo = case.get("demographic_features", {})
        ctx  = case.get("context_features", {})
        conds = case.get("condition_features", [])

        # Step 1: Demographic profiling
        self.step_count += 1
        age = demo.get("age")
        gender = demo.get("gender", "unknown")
        deceased = demo.get("deceased", False)
        risk_age = "elderly" if (age and age >= 65) else ("young" if (age and age < 18) else "adult")
        self._log(f"Step {self.step_count}: Demographic profile — {gender}, {age}y, {risk_age}")

        # Step 2: Encounter burden assessment
        self.step_count += 1
        enc_count = ctx.get("total_encounters", 0)
        enc_classes = ctx.get("encounter_classes", [])
        has_icu = "IMP" in enc_classes or "icu" in str(enc_classes).lower()
        has_emergency = "EMER" in enc_classes or "emergency" in str(enc_classes).lower()
        enc_burden = "high" if enc_count > 5 else ("moderate" if enc_count > 2 else "low")
        self._log(f"Step {self.step_count}: Encounter burden — {enc_burden} ({enc_count} total)")

        # Step 3: Condition landscape
        self.step_count += 1
        unique_conditions = list({c.get("display", c.get("code", "")) for c in conds if c.get("display") or c.get("code")})
        condition_count = case.get("condition_count", 0)
        complexity = "high" if condition_count > 5 else ("moderate" if condition_count > 2 else "low")
        self._log(f"Step {self.step_count}: Condition landscape — {condition_count} conditions, complexity={complexity}")

        # Step 4: Temporal context
        self.step_count += 1
        first_enc = ctx.get("first_encounter")
        last_enc = ctx.get("last_encounter")
        care_span_days = None
        if first_enc and last_enc:
            try:
                d1 = datetime.strptime(first_enc, "%Y-%m-%d")
                d2 = datetime.strptime(last_enc, "%Y-%m-%d")
                care_span_days = abs((d2 - d1).days)
            except ValueError:
                pass
        self._log(f"Step {self.step_count}: Care span — {care_span_days} days")

        summary = (
            f"{gender.capitalize()} patient, {age or 'age unknown'} years old ({risk_age} risk group). "
            f"Encounter burden: {enc_burden} ({enc_count} encounters). "
            f"{'ICU admission noted. ' if has_icu else ''}"
            f"{'Emergency presentation noted. ' if has_emergency else ''}"
            f"Clinical complexity: {complexity} ({condition_count} documented conditions). "
            f"{'Deceased. ' if deceased else ''}"
            f"Care span: {care_span_days or 'N/A'} days."
        )

        return {
            "summary": summary,
            "demographic_profile": {
                "age": age,
                "gender": gender,
                "risk_age_group": risk_age,
                "deceased": deceased,
            },
            "encounter_profile": {
                "total": enc_count,
                "burden": enc_burden,
                "has_icu": has_icu,
                "has_emergency": has_emergency,
                "classes": enc_classes,
            },
            "condition_profile": {
                "count": condition_count,
                "complexity": complexity,
                "unique_conditions": unique_conditions[:15],
            },
            "temporal_profile": {
                "first_encounter": first_enc,
                "last_encounter": last_enc,
                "care_span_days": care_span_days,
            },
            "step_count": self.step_count,
        }


# ── Agent 2: Analysis Agent ───────────────────────────────────────────────────

class AnalysisAgent(BaseAgent):
    name = "AnalysisAgent"

    def run(self, inputs: Dict) -> Dict:
        self.step_count = 0
        case = inputs.get("case", {})
        context_output = inputs.get("context_output", {})
        retrieved_cases = inputs.get("retrieved_cases", [])
        self._log("Starting structured analysis…")

        obs  = case.get("observational_features", {})
        meds = case.get("medication_features", [])
        procs = case.get("procedure_features", [])
        conds = case.get("condition_features", [])

        # Step 1: Vital signs analysis
        self.step_count += 1
        vital_flags = []
        for key, stats in obs.items():
            if "vital" in key.lower() or any(v in key.lower() for v in
                ["heart", "blood", "pressure", "temp", "resp", "spo2", "oxygen"]):
                mean_val = stats.get("mean")
                if mean_val is not None:
                    vital_flags.append(f"{key.split('::')[-1]}: mean={mean_val} {stats.get('unit','')}")
        self._log(f"Step {self.step_count}: {len(vital_flags)} vital sign streams identified")

        # Step 2: Lab results analysis
        self.step_count += 1
        lab_flags = []
        for key, stats in obs.items():
            if "lab" in key.lower() or "laboratory" in key.lower():
                lab_flags.append(f"{key.split('::')[-1]}: mean={stats.get('mean')} {stats.get('unit','')}")
        self._log(f"Step {self.step_count}: {len(lab_flags)} laboratory result streams identified")

        # Step 3: Medication burden
        self.step_count += 1
        med_count = case.get("medication_count", 0)
        unique_meds = list({m.get("med_display", m.get("med_code", "")) for m in meds if m.get("med_display") or m.get("med_code")})
        polypharmacy = med_count > 10
        self._log(f"Step {self.step_count}: Medications={med_count}, polypharmacy={polypharmacy}")

        # Step 4: Procedure burden
        self.step_count += 1
        proc_count = case.get("procedure_count", 0)
        unique_procs = list({p.get("display", p.get("code", "")) for p in procs if p.get("display") or p.get("code")})
        self._log(f"Step {self.step_count}: {proc_count} procedures recorded")

        # Step 5: Comparative analysis with retrieved cases
        self.step_count += 1
        comparisons = []
        for rc in retrieved_cases[:3]:
            rc_demo = rc.get("demographic_features", {})
            diff_cond = abs(rc.get("condition_count", 0) - case.get("condition_count", 0))
            diff_med  = abs(rc.get("medication_count", 0) - med_count)
            comparisons.append({
                "case_id": rc.get("entity_id", "?"),
                "gender": rc_demo.get("gender", "?"),
                "age": rc_demo.get("age"),
                "condition_delta": diff_cond,
                "medication_delta": diff_med,
                "similarity_score": rc.get("similarity_score", 0),
            })
        self._log(f"Step {self.step_count}: Compared against {len(comparisons)} retrieved cases")

        # Step 6: Risk stratification
        self.step_count += 1
        risk_score = 0
        enc_burden = context_output.get("encounter_profile", {}).get("burden", "low")
        if enc_burden == "high":   risk_score += 3
        elif enc_burden == "moderate": risk_score += 1
        if context_output.get("encounter_profile", {}).get("has_icu"):   risk_score += 3
        if context_output.get("encounter_profile", {}).get("has_emergency"): risk_score += 2
        complexity = context_output.get("condition_profile", {}).get("complexity", "low")
        if complexity == "high":     risk_score += 3
        elif complexity == "moderate": risk_score += 1
        if polypharmacy:             risk_score += 2
        if context_output.get("demographic_profile", {}).get("deceased"): risk_score += 4
        risk_age = context_output.get("demographic_profile", {}).get("risk_age_group", "adult")
        if risk_age == "elderly":    risk_score += 2

        risk_level = "CRITICAL" if risk_score >= 10 else (
            "HIGH" if risk_score >= 6 else ("MODERATE" if risk_score >= 3 else "LOW")
        )
        self._log(f"Step {self.step_count}: Risk score={risk_score} → level={risk_level}")

        key_findings = (
            f"Risk level: {risk_level} (score={risk_score}). "
            f"Vital sign streams: {len(vital_flags)}. "
            f"Lab streams: {len(lab_flags)}. "
            f"{'Polypharmacy detected. ' if polypharmacy else ''}"
            f"Unique medications: {len(unique_meds)}. "
            f"Procedures: {proc_count}. "
            f"Compared to {len(comparisons)} similar cases."
        )

        return {
            "key_findings": key_findings,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "polypharmacy": polypharmacy,
            "vital_flags": vital_flags[:10],
            "lab_flags": lab_flags[:10],
            "unique_medications": unique_meds[:10],
            "unique_procedures": unique_procs[:10],
            "comparative_cases": comparisons,
            "step_count": self.step_count,
        }


# ── Agent 3: Resource / Planning Agent ───────────────────────────────────────

class ResourcePlanningAgent(BaseAgent):
    name = "ResourcePlanningAgent"

    RISK_ACTION_MAP = {
        "CRITICAL": [
            "Immediate multidisciplinary team consultation",
            "Intensive care monitoring or ICU placement",
            "Comprehensive medication reconciliation",
            "Urgent specialist referrals for active conditions",
            "Daily clinical reassessment protocol",
            "Family/caregiver communication and care planning",
        ],
        "HIGH": [
            "Specialist consultation within 24 hours",
            "Enhanced medication management review",
            "Frequent vital sign monitoring",
            "Comprehensive care plan development",
            "Patient education and discharge planning",
        ],
        "MODERATE": [
            "Regular outpatient follow-up scheduling",
            "Medication adherence counselling",
            "Preventive care screening",
            "Chronic disease management programme enrolment",
        ],
        "LOW": [
            "Standard preventive care",
            "Health maintenance review",
            "Lifestyle modification counselling",
            "Annual wellness check scheduling",
        ],
    }

    def run(self, inputs: Dict) -> Dict:
        self.step_count = 0
        analysis_output = inputs.get("analysis_output", {})
        context_output  = inputs.get("context_output", {})
        case = inputs.get("case", {})
        self._log("Starting resource and care planning…")

        risk_level = analysis_output.get("risk_level", "LOW")
        polypharmacy = analysis_output.get("polypharmacy", False)
        has_icu = context_output.get("encounter_profile", {}).get("has_icu", False)
        has_emergency = context_output.get("encounter_profile", {}).get("has_emergency", False)
        deceased = context_output.get("demographic_profile", {}).get("deceased", False)

        # Step 1: Primary action plan
        self.step_count += 1
        base_actions = self.RISK_ACTION_MAP.get(risk_level, self.RISK_ACTION_MAP["LOW"]).copy()
        self._log(f"Step {self.step_count}: Base action plan for {risk_level} risk — {len(base_actions)} actions")

        # Step 2: Supplementary actions
        self.step_count += 1
        supplementary = []
        if polypharmacy:
            supplementary.append("Pharmacist-led medication review and reconciliation")
        if has_icu:
            supplementary.append("ICU follow-up and critical care monitoring continuation")
        if has_emergency:
            supplementary.append("Emergency care pathway review and rapid response plan")
        if deceased:
            supplementary.append("Retrospective case review for quality improvement")
        self._log(f"Step {self.step_count}: {len(supplementary)} supplementary actions added")

        # Step 3: Resource allocation
        self.step_count += 1
        resources_needed = []
        if risk_level in ("CRITICAL", "HIGH"):
            resources_needed.extend(["ICU Bed", "Senior Physician", "Pharmacist", "Social Worker"])
        if risk_level == "MODERATE":
            resources_needed.extend(["Outpatient Clinic", "Primary Care Physician"])
        if polypharmacy:
            resources_needed.append("Clinical Pharmacist")
        resources_needed = list(set(resources_needed))
        self._log(f"Step {self.step_count}: Resources identified — {resources_needed}")

        # Step 4: Priority timeline
        self.step_count += 1
        timeline = {
            "CRITICAL": "Immediate (0-4 hours)",
            "HIGH": "Urgent (within 24 hours)",
            "MODERATE": "Soon (within 1 week)",
            "LOW": "Routine (next scheduled visit)",
        }.get(risk_level, "Routine")
        self._log(f"Step {self.step_count}: Action timeline — {timeline}")

        all_actions = base_actions + supplementary
        recommendations_text = (
            f"Priority timeline: {timeline}. "
            f"Primary actions: {'; '.join(base_actions[:3])}. "
            f"Resources required: {', '.join(resources_needed) if resources_needed else 'Standard care team'}."
        )

        return {
            "recommendations": recommendations_text,
            "risk_level": risk_level,
            "priority_timeline": timeline,
            "primary_actions": base_actions,
            "supplementary_actions": supplementary,
            "all_actions": all_actions,
            "resources_needed": resources_needed,
            "step_count": self.step_count,
        }


# ── Agent 4: Decision Agent ───────────────────────────────────────────────────

class DecisionAgent(BaseAgent):
    name = "DecisionAgent"

    def __init__(self, config, llm_client):
        super().__init__(config)
        self.llm = llm_client

    def run(self, inputs: Dict) -> Dict:
        self.step_count = 0
        case           = inputs.get("case", {})
        retrieved      = inputs.get("retrieved_cases", [])
        context_out    = inputs.get("context_output", {})
        analysis_out   = inputs.get("analysis_output", {})
        planning_out   = inputs.get("planning_output", {})
        self._log("Starting decision synthesis…")

        # Step 1: Aggregate agent outputs
        self.step_count += 1
        agent_outputs = {
            "context_agent":  context_out,
            "analysis_agent": analysis_out,
            "planning_agent": planning_out,
        }
        self._log(f"Step {self.step_count}: Aggregating {len(agent_outputs)} agent outputs")

        # Step 2: Prepare input summary
        self.step_count += 1
        demo = case.get("demographic_features", {})
        input_summary = (
            f"Patient: {case.get('entity_id','N/A')} | "
            f"{demo.get('gender','?')} | Age: {demo.get('age','?')} | "
            f"Conditions: {case.get('condition_count',0)} | "
            f"Medications: {case.get('medication_count',0)} | "
            f"Encounters: {case.get('encounter_count',0)} | "
            f"Risk: {analysis_out.get('risk_level','UNKNOWN')}"
        )
        self._log(f"Step {self.step_count}: Input summary composed")

        # Step 3: Retrieved case summary
        self.step_count += 1
        retrieved_summary = [
            {
                "entity_id": rc.get("entity_id"),
                "similarity_score": rc.get("similarity_score", 0),
                "conditions": rc.get("condition_count", 0),
                "medications": rc.get("medication_count", 0),
            }
            for rc in retrieved[:5]
        ]
        self._log(f"Step {self.step_count}: {len(retrieved_summary)} retrieved cases summarised")

        # Step 4: LLM call for final synthesis
        self.step_count += 1
        self._log(f"Step {self.step_count}: Calling LLM for final synthesis…")
        raw_llm = self.llm.generate_decision_report(case, retrieved, agent_outputs)

        # Step 5: Parse LLM output
        self.step_count += 1
        parsed = self._parse_llm_response(raw_llm)
        confidence = parsed.get("confidence_level", 0.0)

        # Fallback confidence from risk score
        if confidence == 0.0:
            risk_score = analysis_out.get("risk_score", 0)
            confidence = min(0.95, 0.5 + risk_score * 0.04)

        self._log(f"Step {self.step_count}: Decision synthesised, confidence={confidence:.2f}")

        return {
            "input_summary":             input_summary,
            "retrieved_cases":           retrieved_summary,
            "analytical_interpretation": analysis_out.get("key_findings", ""),
            "decision_outcome":          planning_out.get("recommendations", ""),
            "justification":             parsed.get("justification", planning_out.get("recommendations", "")),
            "confidence_level":          confidence,
            "raw_llm_response":          raw_llm,
            "agent_outputs":             agent_outputs,
            "risk_level":                analysis_out.get("risk_level", "UNKNOWN"),
            "priority_timeline":         planning_out.get("priority_timeline", "Routine"),
            "step_count":                self.step_count,
        }

    @staticmethod
    def _parse_llm_response(response: str) -> Dict:
        """Extract structured fields from free-text LLM response."""
        result = {
            "justification": "",
            "confidence_level": 0.0,
        }
        if not response:
            return result

        lines = response.split("\n")
        in_justification = False
        justification_lines = []

        for line in lines:
            upper = line.strip().upper()
            if "JUSTIFICATION" in upper:
                in_justification = True
                continue
            if "CONFIDENCE LEVEL" in upper or "CONFIDENCE:" in upper:
                in_justification = False
                # Extract numeric confidence
                import re
                nums = re.findall(r"\d+\.?\d*", line)
                if nums:
                    val = float(nums[0])
                    # Normalise if expressed as percentage
                    result["confidence_level"] = val / 100.0 if val > 1 else val
                continue
            if in_justification and line.strip():
                justification_lines.append(line.strip())

        result["justification"] = " ".join(justification_lines[:8])
        return result
