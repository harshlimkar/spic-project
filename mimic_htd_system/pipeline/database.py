"""
Database Manager — SQLite backend for the MIMIC HTD system.
Schema:   cases, retrieved_cases, evaluation_results
"""

import sqlite3
import json
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("DatabaseManager")


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self.connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT NOT NULL UNIQUE,
                    demographic_features TEXT,
                    observational_features TEXT,
                    condition_features TEXT,
                    context_features TEXT,
                    medication_features TEXT,
                    procedure_features TEXT,
                    encounter_count INTEGER DEFAULT 0,
                    observation_count INTEGER DEFAULT 0,
                    condition_count INTEGER DEFAULT 0,
                    medication_count INTEGER DEFAULT 0,
                    procedure_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_cases_entity ON cases(entity_id);

                CREATE TABLE IF NOT EXISTS evaluation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    iteration INTEGER NOT NULL,
                    patient_id TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    execution_time_sec REAL,
                    processing_steps INTEGER,
                    input_summary TEXT,
                    retrieved_cases TEXT,
                    analytical_interpretation TEXT,
                    decision_outcome TEXT,
                    justification TEXT,
                    confidence_level REAL,
                    agent_outputs TEXT,
                    raw_llm_response TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_eval_iter ON evaluation_results(iteration);
                CREATE INDEX IF NOT EXISTS idx_eval_patient ON evaluation_results(patient_id);
                CREATE INDEX IF NOT EXISTS idx_eval_mode ON evaluation_results(mode);

                CREATE TABLE IF NOT EXISTS ingestion_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT,
                    resource_type TEXT,
                    records_processed INTEGER,
                    records_failed INTEGER,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        logger.info(f"Database initialised at {self.db_path}")

    # ── Case CRUD ────────────────────────────────────────────────────────────

    def upsert_case(self, entity_id: str, data: Dict[str, Any]):
        sql = """
            INSERT INTO cases (
                entity_id, demographic_features, observational_features,
                condition_features, context_features, medication_features,
                procedure_features, encounter_count, observation_count,
                condition_count, medication_count, procedure_count
            ) VALUES (
                :entity_id, :demographic_features, :observational_features,
                :condition_features, :context_features, :medication_features,
                :procedure_features, :encounter_count, :observation_count,
                :condition_count, :medication_count, :procedure_count
            )
            ON CONFLICT(entity_id) DO UPDATE SET
                demographic_features   = excluded.demographic_features,
                observational_features = excluded.observational_features,
                condition_features     = excluded.condition_features,
                context_features       = excluded.context_features,
                medication_features    = excluded.medication_features,
                procedure_features     = excluded.procedure_features,
                encounter_count        = excluded.encounter_count,
                observation_count      = excluded.observation_count,
                condition_count        = excluded.condition_count,
                medication_count       = excluded.medication_count,
                procedure_count        = excluded.procedure_count
        """
        params = {
            "entity_id": entity_id,
            "demographic_features":   json.dumps(data.get("demographic_features", {})),
            "observational_features": json.dumps(data.get("observational_features", {})),
            "condition_features":     json.dumps(data.get("condition_features", [])),
            "context_features":       json.dumps(data.get("context_features", {})),
            "medication_features":    json.dumps(data.get("medication_features", [])),
            "procedure_features":     json.dumps(data.get("procedure_features", [])),
            "encounter_count":        data.get("encounter_count", 0),
            "observation_count":      data.get("observation_count", 0),
            "condition_count":        data.get("condition_count", 0),
            "medication_count":       data.get("medication_count", 0),
            "procedure_count":        data.get("procedure_count", 0),
        }
        with self.connection() as conn:
            conn.execute(sql, params)

    def get_case(self, entity_id: str) -> Optional[Dict]:
        with self.connection() as conn:
            row = conn.execute(
                "SELECT * FROM cases WHERE entity_id = ?", (entity_id,)
            ).fetchone()
        return self._row_to_dict(row) if row else None

    def get_all_patient_ids(self) -> List[str]:
        with self.connection() as conn:
            rows = conn.execute("SELECT entity_id FROM cases").fetchall()
        return [r["entity_id"] for r in rows]

    def get_case_count(self) -> int:
        with self.connection() as conn:
            return conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]

    def retrieve_similar_cases(self, entity_id: str, top_k: int = 5) -> List[Dict]:
        """
        SQL-based RAG retrieval:
        Find patients with similar condition/observation/medication counts and
        overlapping conditions (simple text overlap on condition_features JSON).
        Returns top_k most similar cases (excluding the query patient).
        """
        target = self.get_case(entity_id)
        if not target:
            return []

        raw_cf = target["condition_features"]
        if isinstance(raw_cf, str):
            try:
                raw_cf = json.loads(raw_cf or "[]")
            except Exception:
                raw_cf = []
        target_conditions = set(c.get("code", "") for c in (raw_cf or []))
        target_cond_count  = target["condition_count"]
        target_obs_count   = target["observation_count"]
        target_med_count   = target["medication_count"]

        # Tolerance window ±50% for numeric counts
        sql = """
            SELECT *,
                ABS(condition_count  - :cc) as d_cond,
                ABS(observation_count - :oc) as d_obs,
                ABS(medication_count  - :mc) as d_med
            FROM cases
            WHERE entity_id != :eid
            ORDER BY (d_cond + d_obs + d_med) ASC
            LIMIT :k
        """
        with self.connection() as conn:
            rows = conn.execute(sql, {
                "cc": target_cond_count,
                "oc": target_obs_count,
                "mc": target_med_count,
                "eid": entity_id,
                "k": top_k * 3,
            }).fetchall()

        # Re-rank by condition code overlap
        scored = []
        for row in rows:
            row_dict = self._row_to_dict(row)
            raw_rc = row_dict["condition_features"]
            if isinstance(raw_rc, str):
                try:
                    raw_rc = json.loads(raw_rc or "[]")
                except Exception:
                    raw_rc = []
            row_conditions = set(c.get("code", "") for c in (raw_rc or []))
            overlap = len(target_conditions & row_conditions)
            row_dict["similarity_score"] = overlap
            scored.append(row_dict)

        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]

    # ── Evaluation Results ────────────────────────────────────────────────────

    def save_evaluation_result(self, data: Dict[str, Any]):
        sql = """
            INSERT INTO evaluation_results (
                iteration, patient_id, mode, execution_time_sec,
                processing_steps, input_summary, retrieved_cases,
                analytical_interpretation, decision_outcome, justification,
                confidence_level, agent_outputs, raw_llm_response
            ) VALUES (
                :iteration, :patient_id, :mode, :execution_time_sec,
                :processing_steps, :input_summary, :retrieved_cases,
                :analytical_interpretation, :decision_outcome, :justification,
                :confidence_level, :agent_outputs, :raw_llm_response
            )
        """
        with self.connection() as conn:
            conn.execute(sql, {
                "iteration":                data.get("iteration"),
                "patient_id":               data.get("patient_id"),
                "mode":                     data.get("mode"),
                "execution_time_sec":       data.get("execution_time_sec"),
                "processing_steps":         data.get("processing_steps"),
                "input_summary":            data.get("input_summary", ""),
                "retrieved_cases":          json.dumps(data.get("retrieved_cases", [])),
                "analytical_interpretation":data.get("analytical_interpretation", ""),
                "decision_outcome":         data.get("decision_outcome", ""),
                "justification":            data.get("justification", ""),
                "confidence_level":         data.get("confidence_level", 0.0),
                "agent_outputs":            json.dumps(data.get("agent_outputs", {})),
                "raw_llm_response":         data.get("raw_llm_response", ""),
            })

    def get_all_results(self) -> List[Dict]:
        with self.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM evaluation_results ORDER BY iteration, mode"
            ).fetchall()
        return [dict(r) for r in rows]

    def log_ingestion(self, file_name: str, resource_type: str,
                      records_processed: int, records_failed: int):
        with self.connection() as conn:
            conn.execute(
                """INSERT INTO ingestion_log
                   (file_name, resource_type, records_processed, records_failed)
                   VALUES (?,?,?,?)""",
                (file_name, resource_type, records_processed, records_failed),
            )

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict:
        d = dict(row)
        for key in ("demographic_features", "observational_features",
                    "condition_features", "context_features",
                    "medication_features", "procedure_features"):
            if isinstance(d.get(key), str):
                try:
                    d[key] = json.loads(d[key])
                except (json.JSONDecodeError, TypeError):
                    pass
        return d
