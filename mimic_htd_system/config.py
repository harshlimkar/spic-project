"""
Configuration Module
Centralises all system parameters, paths, and constants.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    # ── Paths ───────────────────────────────────────────────────────────────
    dataset_dir: str = "dataset"
    db_path: str = "trauma.db"
    results_dir: str = "results"
    logs_dir: str = "logs"

    # ── Ollama ───────────────────────────────────────────────────────────────
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_TIMEOUT: int = 120
    OLLAMA_MAX_TOKENS: int = 2048

    # ── RAG ──────────────────────────────────────────────────────────────────
    RAG_TOP_K: int = 5

    # ── FHIR dataset filenames (relative to dataset_dir) ─────────────────────
    PATIENT_FILE: str = "MimicPatient.ndjson"
    CONDITION_FILES: List[str] = field(default_factory=lambda: [
        "MimicCondition.ndjson",
        "MimicConditionED.ndjson",
    ])
    ENCOUNTER_FILES: List[str] = field(default_factory=lambda: [
        "MimicEncounter.ndjson",
        "MimicEncounterED.ndjson",
        "MimicEncounterICU.ndjson",
    ])
    OBSERVATION_FILES: List[str] = field(default_factory=lambda: [
        "MimicObservationChartevents.ndjson",
        "MimicObservationLabevents.ndjson",
        "MimicObservationED.ndjson",
        "MimicObservationVitalSignsED.ndjson",
        "MimicObservationOutputevents.ndjson",
        "MimicObservationDatetimeevents.ndjson",
        "MimicObservationMicroOrg.ndjson",
        "MimicObservationMicroTest.ndjson",
        "MimicObservationMicroSusc.ndjson",
    ])
    MEDICATION_FILES: List[str] = field(default_factory=lambda: [
        "MimicMedicationAdministration.ndjson",
        "MimicMedicationAdministrationICU.ndjson",
        "MimicMedicationRequest.ndjson",
        "MimicMedicationDispense.ndjson",
        "MimicMedicationDispenseED.ndjson",
        "MimicMedicationStatementED.ndjson",
    ])
    PROCEDURE_FILES: List[str] = field(default_factory=lambda: [
        "MimicProcedure.ndjson",
        "MimicProcedureED.ndjson",
        "MimicProcedureICU.ndjson",
    ])

    # ── System modes ─────────────────────────────────────────────────────────
    MODES: List[str] = field(default_factory=lambda: [
        "basic",
        "sequential",
        "semi_coordinated",
        "fully_coordinated",
    ])

    # ── Computed properties ───────────────────────────────────────────────────
    @property
    def DB_PATH(self) -> str:
        return self.db_path

    @property
    def DATASET_DIR(self) -> Path:
        return Path(self.dataset_dir)

    @property
    def RESULTS_DIR(self) -> Path:
        p = Path(self.results_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def __post_init__(self):
        Path(self.results_dir).mkdir(parents=True, exist_ok=True)
        Path(self.logs_dir).mkdir(parents=True, exist_ok=True)

    def find_file(self, filename: str) -> "Path | None":
        """Search recursively for a NDJSON file under dataset_dir (files only)."""
        base = Path(self.dataset_dir)
        matches = [p for p in base.rglob(filename) if p.is_file()]
        return matches[0] if matches else None

    def find_files(self, filenames: List[str]) -> List[Path]:
        found = []
        for name in filenames:
            p = self.find_file(name)
            if p:
                found.append(p)
        return found
