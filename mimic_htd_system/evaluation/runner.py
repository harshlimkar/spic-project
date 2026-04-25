"""
Evaluation Runner
Runs N iterations across all system modes, stores results in SQLite,
and exports a SPSS-ready CSV with one row per (iteration × mode × patient).
"""

import csv
import json
import logging
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger("EvaluationRunner")


class EvaluationRunner:
    def __init__(self, orchestrator, db_manager, config):
        self.orchestrator = orchestrator
        self.db = db_manager
        self.config = config

    def run(
        self,
        iterations: int = 10,
        patient_ids: Optional[List[str]] = None,
    ):
        all_pids = self.db.get_all_patient_ids()
        if not all_pids:
            logger.error("No patient cases in database. Run ingestion first.")
            return

        # Select patient sample
        if patient_ids:
            pids = [p for p in patient_ids if p in all_pids]
        else:
            # One representative patient per iteration
            pids = random.sample(all_pids, min(iterations, len(all_pids)))

        logger.info(
            f"Starting evaluation: {iterations} iterations × "
            f"{len(self.config.MODES)} modes × {len(pids)} patients"
        )

        all_results = []
        for iteration in range(1, iterations + 1):
            patient_id = pids[(iteration - 1) % len(pids)]
            logger.info(f"\n{'='*60}")
            logger.info(f"Iteration {iteration}/{iterations} — Patient: {patient_id}")

            for mode in self.config.MODES:
                logger.info(f"  Running mode: {mode}")
                try:
                    result = self.orchestrator.run_mode(patient_id, mode)
                    result["iteration"] = iteration

                    # Store in DB
                    self.db.save_evaluation_result(result)

                    # Collect for CSV
                    all_results.append(self._flatten_result(result, iteration))

                    logger.info(
                        f"  [{mode}] Time={result.get('execution_time_sec','?'):.3f}s "
                        f"Steps={result.get('processing_steps','?')} "
                        f"Confidence={result.get('confidence_level','?'):.2f}"
                    )
                except Exception as e:
                    logger.error(f"  [{mode}] ERROR: {e}", exc_info=True)

        # Export CSV
        csv_path = self._export_csv(all_results)
        logger.info(f"\nResults exported to: {csv_path}")
        self._print_summary(all_results)

    def _flatten_result(self, result: Dict, iteration: int) -> Dict:
        """Produce a flat dict suitable for a CSV row (SPSS-compatible)."""
        agent_out = result.get("agent_outputs", {})
        ctx = agent_out.get("context_agent", {})
        ana = agent_out.get("analysis_agent", {})
        pln = agent_out.get("planning_agent", {})

        enc_profile = ctx.get("encounter_profile", {})
        dem_profile = ctx.get("demographic_profile", {})
        cond_profile = ctx.get("condition_profile", {})
        temporal = ctx.get("temporal_profile", {})

        return {
            # ── Identifiers ──────────────────────────────────────────────
            "iteration":           iteration,
            "patient_id":          result.get("patient_id", ""),
            "mode":                result.get("mode", ""),

            # ── Performance metrics ──────────────────────────────────────
            "execution_time_sec":  result.get("execution_time_sec", 0.0),
            "processing_steps":    result.get("processing_steps", 0),
            "confidence_level":    round(result.get("confidence_level", 0.0), 7),

            # ── Demographic features ─────────────────────────────────────
            "patient_age":         dem_profile.get("age", ""),
            "patient_gender":      dem_profile.get("gender", ""),
            "risk_age_group":      dem_profile.get("risk_age_group", ""),
            "patient_deceased":    int(dem_profile.get("deceased", False)),

            # ── Clinical features ────────────────────────────────────────
            "condition_count":     cond_profile.get("count", 0),
            "condition_complexity": cond_profile.get("complexity", ""),
            "encounter_total":     enc_profile.get("total", 0),
            "encounter_burden":    enc_profile.get("burden", ""),
            "has_icu_encounter":   int(enc_profile.get("has_icu", False)),
            "has_emergency":       int(enc_profile.get("has_emergency", False)),
            "care_span_days":      temporal.get("care_span_days", ""),

            # ── Analysis outputs ─────────────────────────────────────────
            "risk_score":          ana.get("risk_score", 0),
            "risk_level":          ana.get("risk_level", ""),
            "polypharmacy":        int(ana.get("polypharmacy", False)),
            "vital_streams_count": len(ana.get("vital_flags", [])),
            "lab_streams_count":   len(ana.get("lab_flags", [])),
            "unique_meds_count":   len(ana.get("unique_medications", [])),
            "unique_procs_count":  len(ana.get("unique_procedures", [])),
            "retrieved_cases_count": len(result.get("retrieved_cases", [])),

            # ── Planning outputs ─────────────────────────────────────────
            "priority_timeline":   pln.get("priority_timeline", ""),
            "actions_count":       len(pln.get("all_actions", [])),
            "resources_count":     len(pln.get("resources_needed", [])),

            # ── Decision outputs ─────────────────────────────────────────
            "decision_outcome":    result.get("decision_outcome", "")[:200],
            "justification":       result.get("justification", "")[:200],
            "analytical_interpretation": result.get("analytical_interpretation", "")[:200],

            # ── Mode comparison flags (binary for SPSS ANOVA) ────────────
            "mode_basic":              int(result.get("mode") == "basic"),
            "mode_sequential":         int(result.get("mode") == "sequential"),
            "mode_semi_coordinated":   int(result.get("mode") == "semi_coordinated"),
            "mode_fully_coordinated":  int(result.get("mode") == "fully_coordinated"),
        }

    def _export_csv(self, rows: List[Dict]) -> Path:
        if not rows:
            logger.warning("No results to export.")
            return Path()

        csv_path = self.config.RESULTS_DIR / "evaluation_results.csv"
        fieldnames = list(rows[0].keys())

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"CSV exported: {csv_path} ({len(rows)} rows)")

        # Also export summary statistics
        self._export_summary_stats(rows)
        return csv_path

    def _export_summary_stats(self, rows: List[Dict]):
        """Export per-mode aggregate stats for SPSS/Excel analysis."""
        from collections import defaultdict

        mode_stats = defaultdict(lambda: {
            "n": 0, "total_time": 0.0, "total_steps": 0,
            "total_confidence": 0.0, "total_risk_score": 0
        })

        for row in rows:
            m = row["mode"]
            mode_stats[m]["n"]                 += 1
            mode_stats[m]["total_time"]        += float(row.get("execution_time_sec", 0))
            mode_stats[m]["total_steps"]       += int(row.get("processing_steps", 0))
            mode_stats[m]["total_confidence"]  += float(row.get("confidence_level", 0))
            mode_stats[m]["total_risk_score"]  += float(row.get("risk_score", 0))

        summary_path = self.config.RESULTS_DIR / "mode_summary_stats.csv"
        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "mode", "n", "mean_execution_time_sec",
                "mean_processing_steps", "mean_confidence",
                "mean_risk_score",
            ])
            writer.writeheader()
            for mode, s in mode_stats.items():
                n = s["n"] or 1
                writer.writerow({
                    "mode": mode,
                    "n": s["n"],
                    "mean_execution_time_sec": round(s["total_time"] / n, 4),
                    "mean_processing_steps":   round(s["total_steps"] / n, 2),
                    "mean_confidence":         round(s["total_confidence"] / n, 4),
                    "mean_risk_score":         round(s["total_risk_score"] / n, 2),
                })

        logger.info(f"Summary stats exported: {summary_path}")

    def _print_summary(self, rows: List[Dict]):
        from collections import defaultdict
        mode_conf = defaultdict(list)
        mode_time = defaultdict(list)
        mode_steps = defaultdict(list)

        for row in rows:
            m = row["mode"]
            mode_conf[m].append(float(row.get("confidence_level", 0)))
            mode_time[m].append(float(row.get("execution_time_sec", 0)))
            mode_steps[m].append(int(row.get("processing_steps", 0)))

        logger.info("\n" + "="*70)
        logger.info("EVALUATION SUMMARY")
        logger.info("="*70)
        logger.info(f"{'Mode':<25} {'Avg Time(s)':<14} {'Avg Steps':<12} {'Avg Confidence'}")
        logger.info("-"*70)
        for mode in self.config.MODES:
            if mode in mode_conf:
                avg_t = sum(mode_time[mode]) / len(mode_time[mode])
                avg_s = sum(mode_steps[mode]) / len(mode_steps[mode])
                avg_c = sum(mode_conf[mode]) / len(mode_conf[mode])
                logger.info(f"{mode:<25} {avg_t:<14.4f} {avg_s:<12.1f} {avg_c:.4f}")
        logger.info("="*70)
