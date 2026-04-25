"""
Ollama LLM Client
Wraps the local Ollama REST API for llama3 inference.
Falls back to a deterministic template response when Ollama is unavailable.
"""

import json
import logging
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

logger = logging.getLogger("OllamaClient")


class OllamaClient:
    def __init__(self, config):
        self.url     = config.OLLAMA_URL
        self.model   = config.OLLAMA_MODEL
        self.timeout = config.OLLAMA_TIMEOUT
        self._available: Optional[bool] = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            health_url = self.url.replace("/api/generate", "/api/tags")
            req = urllib.request.Request(health_url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                self._available = resp.status == 200
        except Exception:
            self._available = False
            logger.warning("Ollama not reachable — using fallback template mode.")
        return self._available

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.is_available():
            return self._fallback_response(prompt)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "num_predict": 2048,
                "temperature": 0.3,
                "top_p": 0.9,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                result = json.loads(body)
                return result.get("response", "")
        except urllib.error.URLError as e:
            logger.error(f"Ollama request failed: {e}")
            return self._fallback_response(prompt)
        except json.JSONDecodeError as e:
            logger.error(f"Ollama JSON decode error: {e}")
            return self._fallback_response(prompt)

    def generate_decision_report(
        self,
        case_data: Dict,
        retrieved_cases: list,
        agent_outputs: Dict,
    ) -> str:
        """Compose a structured clinical decision report via LLM."""

        demo = case_data.get("demographic_features", {})
        conds = case_data.get("condition_features", [])
        obs   = case_data.get("observational_features", {})
        meds  = case_data.get("medication_features", [])
        procs = case_data.get("procedure_features", [])
        ctx   = case_data.get("context_features", {})

        # Summarise top conditions
        cond_list = [c.get("display", c.get("code", "")) for c in conds[:10]]
        med_list  = list({m.get("med_display", m.get("med_code", "")) for m in meds[:8]})
        proc_list = list({p.get("display", p.get("code", "")) for p in procs[:5]})

        # Summarise retrieved context
        ret_summary = []
        for rc in retrieved_cases[:3]:
            rc_demo = rc.get("demographic_features", {})
            ret_summary.append(
                f"  • Patient {rc.get('entity_id','?')}: "
                f"{rc_demo.get('gender','?')}, age {rc_demo.get('age','?')}, "
                f"{rc.get('condition_count',0)} conditions, "
                f"{rc.get('medication_count',0)} medications"
            )

        system_prompt = (
            "You are a senior clinical AI decision support system. "
            "Analyse the patient case and generate a structured clinical decision report. "
            "Be precise, evidence-based, and clinically appropriate. "
            "Output sections: INPUT SUMMARY, RETRIEVED CONTEXT, ANALYTICAL INTERPRETATION, "
            "DECISION OUTCOME, JUSTIFICATION, CONFIDENCE LEVEL (0-1)."
        )

        prompt = f"""
PATIENT CASE ANALYSIS REQUEST
==============================
Patient ID: {case_data.get('entity_id', 'Unknown')}
Gender: {demo.get('gender', 'unknown')} | Age: {demo.get('age', 'unknown')} | 
Deceased: {demo.get('deceased', False)} | Marital: {demo.get('marital_status','unknown')}

ENCOUNTER CONTEXT:
- Total encounters: {ctx.get('total_encounters', 0)}
- Encounter classes: {', '.join(ctx.get('encounter_classes', []))}
- First visit: {ctx.get('first_encounter', 'N/A')}
- Last visit: {ctx.get('last_encounter', 'N/A')}
- Discharge dispositions: {', '.join(ctx.get('discharge_dispositions', []))}

CONDITIONS ({case_data.get('condition_count', 0)} total):
{chr(10).join('- ' + c for c in cond_list) if cond_list else '- None recorded'}

MEDICATIONS ({case_data.get('medication_count', 0)} total):
{chr(10).join('- ' + m for m in med_list) if med_list else '- None recorded'}

PROCEDURES ({case_data.get('procedure_count', 0)} total):
{chr(10).join('- ' + p for p in proc_list) if proc_list else '- None recorded'}

RETRIEVED SIMILAR CASES (RAG):
{chr(10).join(ret_summary) if ret_summary else '- No similar cases found'}

AGENT ANALYSIS OUTPUTS:
- Context Agent: {agent_outputs.get('context_agent', {}).get('summary', 'N/A')}
- Analysis Agent: {agent_outputs.get('analysis_agent', {}).get('key_findings', 'N/A')}
- Planning Agent: {agent_outputs.get('planning_agent', {}).get('recommendations', 'N/A')}

Please generate a comprehensive clinical decision report with all six sections.
Conclude with CONFIDENCE LEVEL as a decimal between 0.0 and 1.0.
"""
        return self.generate(prompt, system_prompt)

    @staticmethod
    def _fallback_response(prompt: str) -> str:
        """Deterministic fallback when Ollama is offline."""
        return (
            "INPUT SUMMARY:\n"
            "Patient clinical data has been processed and structured for analysis.\n\n"
            "RETRIEVED CONTEXT:\n"
            "Similar cases have been retrieved from the RAG knowledge base "
            "to provide contextual reference for this decision.\n\n"
            "ANALYTICAL INTERPRETATION:\n"
            "The multi-agent system has evaluated the patient's clinical profile "
            "including demographics, conditions, medications, procedures, and encounter history. "
            "The hierarchical task decomposition identified key clinical signals and risk factors.\n\n"
            "DECISION OUTCOME:\n"
            "Based on the available clinical evidence, this patient requires careful monitoring "
            "and evidence-based clinical intervention aligned with their documented conditions.\n\n"
            "JUSTIFICATION:\n"
            "The decision is supported by the patient's clinical history, retrieved similar cases, "
            "and structured multi-agent reasoning across all available data domains.\n\n"
            "CONFIDENCE LEVEL: 0.72\n"
            "[NOTE: Generated in offline/fallback mode — Ollama LLM not available]"
        )
