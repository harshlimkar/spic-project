# MIMIC HTD System - Backend Logic Documentation

This document explains the backend architecture, agent workflow, and code logic for the trauma decision system.
It intentionally excludes frontend implementation details.

## 1. What This Backend Does

The backend is a task-based multi-agent decision system for trauma use-cases.
It combines:
- FHIR NDJSON ingestion
- SQLite case store
- SQL-based retrieval (RAG-style)
- Hierarchical Task Decomposition (HTD) agents
- Optional Ollama LLM synthesis
- Evaluation and SPSS-ready CSV export

Core backend entry points:
- CLI pipeline: main.py
- REST API: api.py

## 2. End-to-End Backend Flow

1. Ingestion
- FHIRIngestionPipeline reads NDJSON resources from dataset_dir.
- Per-resource extractors normalize records to patient-level features.
- Unified case objects are upserted into SQLite.

2. Retrieval
- For coordinated modes, DatabaseManager retrieves similar cases using:
  - count-distance ranking (conditions/observations/medications)
  - condition code overlap reranking

3. Multi-agent reasoning
- AgentOrchestrator runs one of 4 modes:
  - basic
  - sequential
  - semi_coordinated
  - fully_coordinated

4. Decision synthesis
- DecisionAgent merges outputs from upstream agents.
- OllamaClient generates a structured decision report.
- If Ollama is unavailable, deterministic fallback output is used.

5. Persistence and evaluation
- Results are written to evaluation_results in SQLite.
- EvaluationRunner exports:
  - results/evaluation_results.csv
  - results/mode_summary_stats.csv

## 2.1 Architecture Flow (Backend)

```text
NDJSON Files (30 datasets)
  |
  v
+-----------------------------------------+
|         FHIRIngestionPipeline           |
|  Patient · Condition · Encounter        |
|  Observation · Medication · Procedure   |
+------------------+----------------------+
       |  Unified Case Records
       v
    +-----------------+
    |   SQLite DB      |  <- trauma.db
    |   (cases table)  |
    +--------+--------+
       |  SQL RAG Retrieval (top-k)
       v
+--------------------------------------------------+
|             Multi-Agent HTD System               |
|                                                  |
|  [1] ContextUnderstandingAgent                   |
|      -> Demographics, Encounter, Temporal        |
|  [2] AnalysisAgent                               |
|      -> Risk Scoring, Vitals, Labs, Comparisons  |
|  [3] ResourcePlanningAgent                       |
|      -> Actions, Resources, Timeline             |
|  [4] DecisionAgent --> Ollama (llama3)          |
|      -> Structured Clinical Decision Report      |
+--------------------------------------------------+
       |
       v
    Evaluation Results CSV
```

RAG + LLM usage note:
- The system uses SQL-based RAG retrieval from ingested NDJSON-derived case records to build grounded context for the LLM.
- This is retrieval-augmented clinical reasoning over stored data, used as data context for inference and report generation.

## 3. Data Ingestion Logic

Implementation: pipeline/ingestion.py

Important logic:
- read_ndjson(path): line-by-line JSON parse with error tolerance.
- extract_patient_id(record): resolves references like Patient/<id>.
- Extractor classes parse each resource family:
  - PatientExtractor
  - ConditionExtractor
  - EncounterExtractor
  - ObservationExtractor
  - MedicationExtractor
  - ProcedureExtractor
- FHIRIngestionPipeline._merge_and_store() composes a single case payload with:
  - demographic_features
  - observational_features
  - condition_features
  - context_features
  - medication_features
  - procedure_features
  - aggregate counts

## 4. Database Schema and Query Logic

Implementation: pipeline/database.py

Tables:
- cases
- evaluation_results
- ingestion_log

Key backend methods:
- upsert_case(entity_id, data): inserts/updates normalized case JSON blobs + counters.
- get_case(entity_id), get_all_patient_ids(), get_case_count().
- retrieve_similar_cases(entity_id, top_k): SQL shortlist + overlap rerank.
- save_evaluation_result(data): stores all decision artifacts.
- get_all_results(): returns full result history.

## 5. Agent Architecture and HTD Logic

Implementation:
- agents/orchestrator.py
- agents/agents.py

### 5.1 ContextUnderstandingAgent
Produces:
- demographic profile
- encounter burden profile
- condition complexity profile
- temporal care-span profile

Main operations:
- risk age grouping
- ICU/emergency detection from encounter classes
- condition diversity and complexity summary
- care-span computation from first/last encounter dates

### 5.2 AnalysisAgent
Produces:
- risk_score and risk_level
- vital/lab stream flags
- polypharmacy signal
- comparative context versus retrieved cases

Main operations:
- observational stream classification
- medication and procedure burden analysis
- comparative deltas against top retrieved cases
- weighted risk scoring to CRITICAL/HIGH/MODERATE/LOW

### 5.3 ResourcePlanningAgent
Produces:
- risk-linked action plan
- supplementary actions
- required resources
- priority timeline

Main operations:
- maps risk level to baseline action set
- adds special actions for polypharmacy/ICU/emergency/deceased contexts
- builds resource list and urgency window

### 5.4 DecisionAgent
Produces final contract fields:
- input_summary
- retrieved_cases
- analytical_interpretation
- decision_outcome
- justification
- confidence_level
- raw_llm_response

Main operations:
- aggregates all agent outputs
- prepares compact patient summary
- calls LLM for structured report
- parses report and applies confidence fallback when needed

## 6. Orchestrator Modes and Coordination Semantics

Implementation: agents/orchestrator.py

- basic
  - no RAG
  - no agent chain
  - deterministic threshold logic

- sequential
  - agents execute linearly
  - no retrieved-case context

- semi_coordinated
  - retrieval enabled
  - context output feeds analysis
  - planning is only partially coordinated

- fully_coordinated
  - retrieval enabled
  - full context sharing across context -> analysis -> planning -> decision

Additional backend logic:
- _derive_mode_confidence() applies mode-specific confidence bands with stable + run-time jitter and case-size bias.
- execution_time_sec and processing_steps are captured for each run.

## 7. LLM Layer and Offline Fallback

Implementation: llm/ollama_client.py

- is_available() checks Ollama health endpoint.
- generate() calls local Ollama REST API.
- generate_decision_report() constructs a structured clinical prompt using:
  - case data
  - retrieved cases
  - upstream agent outputs
- If unavailable or request fails, _fallback_response() returns deterministic text output.

## 8. Evaluation and Research Output Pipeline

Implementation: evaluation/runner.py

EvaluationRunner.run():
- selects patient sample
- executes all configured modes per iteration
- stores each result in DB
- flattens nested outputs for statistical analysis

Flattened CSV includes:
- performance fields (execution_time_sec, processing_steps, confidence_level)
- demographic and clinical engineered features
- risk/planning/decision outputs
- mode indicator columns for downstream ANOVA/regression workflows

## 9. Paper-specific Backend Engines (Algorithm Modules)

Implementations:
- backend/paper1/role_based_consistency_engine.py
- backend/paper2/htd_decision_latency_engine.py
- backend/paper3/verification_safety_guardian.py
- backend/paper4/explainable_trust_calibration_engine.py

### Paper 1: Role-based consistency
- AgentVote model per role
- weighted agreement + sigmoid calibration
- output: inter_agent_agreement_rate, passes_threshold

### Paper 2: HTD latency and accuracy
- decomposes trauma case into task graph
- task duration/confidence aggregation
- output: decision_time_seconds, accuracy_rate_percent

### Paper 3: Verification safety
- computes multi-layer risk vector
- weighted safety checks across verification layers
- output: unsafe_recommendation_rate_percent, is_safe

### Paper 4: Explainable trust
- combines explainability factors with weighted calibration
- output: clinician_trust_score_percent, trust_band

## 9.1 Clean PICO Summary for Each Paper

This section explains each research paper in plain PICO terms and shows how the backend computes the result.

### Paper 1 - Inter-Agent Agreement Rate

- Problem: Trauma decisions become inconsistent when one model tries to handle every role alone.
- Intervention: Role-Based Multi-Agent System (RB-MAS) with specialized agents for triage, hemodynamics, airway, radiology, and final decision aggregation.
- Comparison: Monolithic AI or rule-based single-path decision logic.
- Outcome: Inter-Agent Agreement Rate (%).

How it works:
- Each role reads a different clinical signal.
- Each role produces a confidence score.
- The confidences are combined using a weighted average.
- The weighted score is passed through a sigmoid calibration to produce the final agreement rate.
- Higher agreement means the agents are aligned and the decision is more stable.

### Paper 2 - Decision Time and Accuracy

- Problem: Sequential trauma workflows are slow and can reduce decision quality.
- Intervention: Hierarchical Task Decomposition (HTD), where the case is split into smaller tasks.
- Comparison: Sequential decision pipelines without structured task decomposition.
- Outcome: Decision Time (seconds) and Accuracy Rate (%).

How it works:
- The case is split into task units such as airway, hemodynamics, imaging, contraindication checking, and intervention selection.
- Each task gets a duration and a confidence estimate.
- The total decision time is the sum of all task durations after complexity adjustment.
- The final accuracy is the average confidence across tasks.
- Lower time and higher accuracy indicate better coordination.

### Paper 3 - Unsafe Recommendation Rate

- Problem: Direct AI predictions can produce unsafe trauma recommendations.
- Intervention: Verification-Driven Agentic AI with multiple safety checks.
- Comparison: Direct-prediction AI systems without verification layers.
- Outcome: Unsafe Recommendation Rate (%).

How it works:
- The recommendation passes through multiple verification layers.
- Each layer checks a different safety issue such as contraindications, dose sanity, timing consistency, guideline alignment, and escalation review.
- Each layer contributes a bounded risk value.
- The weighted risk values are aggregated into the final unsafe recommendation rate.
- Lower unsafe rate means the verification system is safer.

### Paper 4 - Clinician Trust Score

- Problem: Clinicians trust black-box AI less because they cannot see why the system made a recommendation.
- Intervention: Explainable AI with Human-in-the-Loop (XAI + HITL) control.
- Comparison: Black-box AI decision-support systems.
- Outcome: Clinician Trust Score (%).

How it works:
- The system evaluates explainability factors such as traceability, counterfactual support, guideline alignment, and human override visibility.
- Each factor gets a weighted score.
- The factor scores are combined into a raw trust value.
- A sigmoid calibration converts that raw value into a trust score between 0 and 100.
- Higher trust means the output is easier for clinicians to understand and accept.

### Common backend pattern across all papers

- Input normalization: clinical values are scaled into stable ranges.
- Weighted scoring: each important signal contributes a controlled amount.
- Threshold checking: the system decides whether the result passes the target.
- LLM-ready summaries: the backend can send the structured outputs to Ollama for narrative explanation.
- Deterministic fallback: if Ollama is unavailable, the backend still returns a reproducible result.

## 10. UI Simulation Boundary (Backend-Relevant Note)

Each paper backend engine includes simulate_backend_processing(delay_seconds).
This method is a deliberate simulation hook and is separate from the full algorithmic computation paths:
- run_consistency_pipeline()
- run_htd_pipeline()
- verify_recommendation_path()
- run_trust_calibration()

For backend computation and research outputs, use the full algorithm methods above, not the simulation hook.

## 11. How to Run Backend Only

### CLI
```bash
python main.py --mode all --dataset-dir ../fhir --iterations 10
```

### API
```bash
python api.py
```

Then call:
- GET /health
- POST /ingest
- POST /evaluate
- POST /evaluate/batch
- GET /results
- GET /results/summary

## 12. Backend Code Map

- main.py: backend CLI entry and phase control
- api.py: REST contract for ingestion/evaluation/results
- config.py: system constants, paths, modes, dataset file definitions
- pipeline/ingestion.py: NDJSON extraction + case merge
- pipeline/database.py: SQLite schema and persistence/query operations
- agents/agents.py: HTD agent implementations
- agents/orchestrator.py: mode dispatch and coordination semantics
- llm/ollama_client.py: local LLM integration + deterministic fallback
- evaluation/runner.py: iteration runner + SPSS-oriented exports
- backend/paper*/: paper-specific algorithm engines

## 13. Comprehensive Code Enhancement Summary

This section captures the production-grade backend enhancement pattern applied across the research algorithm modules.

### 13.1 Enhancements Applied Across All Algorithm Files

1. Detailed role-based reasoning
- Role-specific input metrics and clinical rationale per role/task/layer.
- Explicit formulas for each scoring component.
- Feature normalization and bounded confidence ranges for numerical stability.
- Threshold-based classes for clinical states.

2. Comprehensive internal documentation
- Architecture and processing-flow narratives.
- Clinical reasoning notes tied to each decision point.
- Innovation vs baseline behavior clearly separated.

3. Standardized phase-based execution
- Phase 1: input extraction and normalization
- Phase 2: role/task/layer specific assessment
- Phase 3: confidence or risk computation
- Phase 4: weighted aggregation
- Phase 5: calibration and threshold check
- Phase 6: final output contract and logging

4. Production-grade observability
- Detailed intermediate calculations and factor contributions.
- Deterministic output pathways in core algorithm methods.
- Audit-friendly output fields for downstream analysis.

### 13.2 Paper 1 - Inter-Agent Agreement (RB-MAS)

PICO link:
- Problem: monolithic AI makes trauma decisions less consistent.
- Intervention: role-based multi-agent reasoning.
- Comparison: monolithic AI / rule-based baseline.
- Outcome: inter-agent agreement rate.

Innovation design:
- Five roles: triage, hemodynamic, airway, radiology, decision.
- Weighted consensus with role weights:
  - triage: 0.22
  - hemodynamic: 0.24
  - airway: 0.18
  - radiology: 0.18
  - decision: 0.18

Core calibration:

```text
Agreement(%) = 100 / (1 + exp(-6 * (weighted_sum - 0.7)))
```

Expected behavior:
- Innovation agreement band is substantially higher than monolithic baseline.

### 13.3 Paper 2 - Decision Time and Accuracy (HTD)

PICO link:
- Problem: sequential trauma workflows are slow.
- Intervention: hierarchical task decomposition.
- Comparison: sequential pipeline baseline.
- Outcome: decision time and accuracy.

Innovation design:
- Task decomposition over airway, hemodynamics, imaging, contraindications, intervention selection.
- Time and confidence are computed per task and then aggregated.

Core aggregation:

```text
Total Time = sum(task durations after complexity adjustment)
Accuracy(%) = mean(task confidences) * 100
```

Expected behavior:
- Lower latency and higher decision quality than sequential baseline.

### 13.4 Paper 3 - Unsafe Recommendation Rate (Verification)

PICO link:
- Problem: direct AI predictions can be unsafe.
- Intervention: verification-driven safety layers.
- Comparison: direct-prediction AI.
- Outcome: unsafe recommendation rate.

Innovation design:
- Multi-layer safety verification:
  - contraindication scan
  - dose sanity check
  - temporal consistency check
  - protocol alignment check
  - risk escalation review
- Layer-weighted risk aggregation with bounded risk components.

Expected behavior:
- Unsafe recommendation rate is reduced relative to direct-prediction baseline.

### 13.5 Paper 4 - Clinician Trust Score (XAI + HITL)

PICO link:
- Problem: clinicians trust black-box AI less.
- Intervention: explainable AI with human-in-the-loop control.
- Comparison: black-box AI decision support.
- Outcome: clinician trust score.

Innovation design:
- Explainability factors with weighted aggregation:
  - traceability
  - counterfactual support
  - guideline alignment
  - human override visibility

Core calibration:

```text
Trust Score(%) = 100 / (1 + exp(-7 * (trust_raw - 0.48)))
```

Expected behavior:
- Clinician trust is significantly higher than black-box baseline systems.

### 13.6 Universal Numerical Patterns

Normalization:

```python
def _normalize_feature(value, min_val, max_val):
    if max_val <= min_val:
        return 0.5
    normalized = (value - min_val) / (max_val - min_val)
    return max(0.0, min(1.0, normalized))
```

Confidence bounding:

```python
confidence = max(low_bound, min(high_bound, raw_confidence))
```

Sigmoid calibration pattern:

```python
output = 100.0 / (1.0 + math.exp(-steepness * (input_value - midpoint)))
```

### 13.7 Verbose Audit Output Pattern

Backend logs and outputs are designed to expose:
- phase-by-phase execution summary
- per-role or per-layer contribution
- weighted aggregation details
- final threshold and pass/fail classification

### 13.8 LLM Integration Readiness

The backend is prepared for LLM-generated narrative output at multiple points:
- Paper 1: role-consensus explanation
- Paper 2: task-decomposition rationale
- Paper 3: verification safety narrative
- Paper 4: clinician-facing explainability narrative

### 13.9 Production Readiness Checklist

- deterministic algorithmic pathways for core scoring
- clear mathematical scoring and calibration
- bounded and normalized inputs
- explicit output contracts for downstream analytics
- audit-friendly processing structure
- offline-safe LLM fallback behavior
