"""
Task-Based Multi-Agent Decision System using RAG + Ollama (LLM) + Hierarchical Task Decomposition (HTD)
Main Entry Point
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.ingestion import FHIRIngestionPipeline
from pipeline.database import DatabaseManager
from agents.orchestrator import AgentOrchestrator
from evaluation.runner import EvaluationRunner
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("system.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("Main")


def main():
    parser = argparse.ArgumentParser(
        description="Task-Based Multi-Agent Decision System (MIMIC-FHIR + RAG + Ollama + HTD)"
    )
    parser.add_argument(
        "--mode",
        choices=["ingest", "run", "evaluate", "all"],
        default="all",
        help="Execution mode",
    )
    parser.add_argument(
        "--dataset-dir",
        default="dataset",
        help="Path to NDJSON dataset directory",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of evaluation iterations (default: 10)",
    )
    parser.add_argument(
        "--patient-ids",
        nargs="*",
        help="Specific patient IDs to process (optional)",
    )
    args = parser.parse_args()

    config = Config(dataset_dir=args.dataset_dir)
    db_manager = DatabaseManager(config.DB_PATH)

    if args.mode in ("ingest", "all"):
        logger.info("=== PHASE 1: Data Ingestion ===")
        pipeline = FHIRIngestionPipeline(config, db_manager)
        pipeline.run()
        logger.info("Ingestion complete.")

    if args.mode in ("run", "evaluate", "all"):
        logger.info("=== PHASE 2: Multi-Agent Evaluation ===")
        orchestrator = AgentOrchestrator(config, db_manager)
        runner = EvaluationRunner(orchestrator, db_manager, config)
        runner.run(iterations=args.iterations, patient_ids=args.patient_ids)
        logger.info("Evaluation complete. Results saved to results/")


if __name__ == "__main__":
    main()
