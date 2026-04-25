"""
FastAPI Backend — REST API for the MIMIC HTD Decision System
Endpoints:
  POST /ingest          — run data ingestion
  GET  /patients        — list all patient IDs
  GET  /patients/{id}   — get patient case details
  POST /evaluate        — run evaluation (one patient, one mode)
  POST /evaluate/batch  — run full multi-iteration evaluation
  GET  /results         — get all evaluation results
  GET  /health          — system health check
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import json

from config import Config
from pipeline.database import DatabaseManager
from pipeline.ingestion import FHIRIngestionPipeline
from agents.orchestrator import AgentOrchestrator
from evaluation.runner import EvaluationRunner

logger = logging.getLogger("FastAPI")

app = FastAPI(
    title="MIMIC HTD Multi-Agent Decision System",
    description="Task-Based Multi-Agent Decision System using RAG + Ollama + HTD",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Shared singletons ─────────────────────────────────────────────────────────

config       = Config()
db_manager   = DatabaseManager(config.DB_PATH)
orchestrator = AgentOrchestrator(config, db_manager)


# ── Request/Response models ───────────────────────────────────────────────────

class IngestRequest(BaseModel):
    dataset_dir: Optional[str] = "dataset"

class EvaluateRequest(BaseModel):
    patient_id: str
    mode: str = "fully_coordinated"

class BatchEvaluateRequest(BaseModel):
    iterations: int = 10
    patient_ids: Optional[List[str]] = None

class HealthResponse(BaseModel):
    status: str
    cases_in_db: int
    ollama_available: bool
    modes: List[str]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
def health_check():
    from llm.ollama_client import OllamaClient
    llm = OllamaClient(config)
    return HealthResponse(
        status="ok",
        cases_in_db=db_manager.get_case_count(),
        ollama_available=llm.is_available(),
        modes=config.MODES,
    )


@app.post("/ingest")
def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    cfg = Config(dataset_dir=request.dataset_dir)
    pipeline = FHIRIngestionPipeline(cfg, db_manager)
    background_tasks.add_task(pipeline.run)
    return {"message": "Ingestion started in background", "dataset_dir": request.dataset_dir}


@app.get("/patients")
def list_patients():
    pids = db_manager.get_all_patient_ids()
    return {"count": len(pids), "patient_ids": pids}


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    case = db_manager.get_case(patient_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    return case


@app.get("/patients/{patient_id}/similar")
def get_similar(patient_id: str, k: int = 5):
    similar = db_manager.retrieve_similar_cases(patient_id, k)
    return {"patient_id": patient_id, "retrieved_k": len(similar), "cases": similar}


@app.post("/evaluate")
def evaluate(request: EvaluateRequest):
    if request.mode not in config.MODES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode '{request.mode}'. Valid: {config.MODES}"
        )
    result = orchestrator.run_mode(request.patient_id, request.mode)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.post("/evaluate/all-modes")
def evaluate_all_modes(patient_id: str):
    """Run a patient through all 4 modes and return comparison."""
    results = {}
    for mode in config.MODES:
        results[mode] = orchestrator.run_mode(patient_id, mode)
    return {"patient_id": patient_id, "mode_comparison": results}


@app.post("/evaluate/batch")
def batch_evaluate(request: BatchEvaluateRequest, background_tasks: BackgroundTasks):
    runner = EvaluationRunner(orchestrator, db_manager, config)
    background_tasks.add_task(
        runner.run,
        iterations=request.iterations,
        patient_ids=request.patient_ids,
    )
    return {
        "message": "Batch evaluation started in background",
        "iterations": request.iterations,
    }


@app.get("/results")
def get_results():
    rows = db_manager.get_all_results()
    return {"count": len(rows), "results": rows}


@app.get("/results/summary")
def get_results_summary():
    rows = db_manager.get_all_results()
    from collections import defaultdict
    mode_stats = defaultdict(lambda: {"n": 0, "total_time": 0.0,
                                       "total_steps": 0, "total_confidence": 0.0})
    for row in rows:
        m = row.get("mode", "unknown")
        mode_stats[m]["n"]                += 1
        mode_stats[m]["total_time"]       += float(row.get("execution_time_sec") or 0)
        mode_stats[m]["total_steps"]      += int(row.get("processing_steps") or 0)
        mode_stats[m]["total_confidence"] += float(row.get("confidence_level") or 0)

    summary = {}
    for mode, s in mode_stats.items():
        n = s["n"] or 1
        summary[mode] = {
            "n": s["n"],
            "mean_execution_time_sec": round(s["total_time"] / n, 4),
            "mean_processing_steps":   round(s["total_steps"] / n, 2),
            "mean_confidence":         round(s["total_confidence"] / n, 4),
        }
    return {"total_results": len(rows), "mode_summary": summary}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
