"""Streamlit research dashboard with simulation UI and production-style backend separation.

Run with:
    streamlit run streamlit_research_dashboard.py
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

import pandas as pd
import streamlit as st

from config import Config
from backend.paper1.role_based_consistency_engine import RoleBasedConsistencyEngine
from backend.paper2.htd_decision_latency_engine import HTDDecisionLatencyEngine
from backend.paper3.verification_safety_guardian import VerificationSafetyGuardian
from backend.paper4.explainable_trust_calibration_engine import ExplainableTrustCalibrationEngine


@dataclass(frozen=True)
class PaperRecord:
    paper_id: str
    tab_name: str
    project_title: str
    problem: str
    intervention: str
    comparison: str
    outcome: str


PAPERS: List[PaperRecord] = [
    PaperRecord(
        paper_id="paper1",
        tab_name="Research Paper 1",
        project_title=(
            "Role-Based Multi-Agent AI Architecture for Trauma Emergency Decisions Compared "
            "to Traditional AI Systems with Improved Decision Consistency"
        ),
        problem="Decision Support Systems for Trauma emergency care",
        intervention="Role-Based Multi-Agent System (RB-MAS)",
        comparison="Monolithic AI architectures and rule-based trauma scoring systems",
        outcome="Inter-Agent Agreement Rate (%)",
    ),
    PaperRecord(
        paper_id="paper2",
        tab_name="Research Paper 2",
        project_title=(
            "Task-Based Multi-Agent Approach for Trauma Emergency Decision-Making Compared "
            "to Uncoordinated Workflows, Reducing Decision Time"
        ),
        problem="Poor coordination in trauma decision-making",
        intervention="Hierarchical Task Decomposition (HTD) with multi-agent planning",
        comparison="Sequential decision pipelines and uncoordinated AI/manual workflows",
        outcome="Average Decision Time (seconds) and Accuracy Rate (%)",
    ),
    PaperRecord(
        paper_id="paper3",
        tab_name="Research Paper 3",
        project_title=(
            "Verification-Based Agentic AI System for Trauma Emergency Decisions Compared to "
            "Standard AI, Reducing Unsafe Recommendations"
        ),
        problem="Unsafe AI decisions in trauma care",
        intervention="Verification-Driven Agentic AI",
        comparison="Direct-prediction AI systems without validation layers",
        outcome="Unsafe Recommendation Rate (%)",
    ),
    PaperRecord(
        paper_id="paper4",
        tab_name="Research Paper 4",
        project_title=(
            "Explainable Human-in-the-Loop Agentic AI System for Trauma Emergency Decisions "
            "Compared to Black-Box AI, Increasing Clinician Trust"
        ),
        problem="Lack of trust in trauma AI systems",
        intervention="Agent-Level Explainable AI (XAI) with Human-in-the-Loop (HITL) control",
        comparison="Black-box AI decision-support systems",
        outcome="Clinician Trust Score (%)",
    ),
]


@st.cache_resource
def get_backend_engines() -> Dict[str, object]:
    cfg = Config()
    return {
        "paper1": RoleBasedConsistencyEngine(config=cfg),
        "paper2": HTDDecisionLatencyEngine(config=cfg),
        "paper3": VerificationSafetyGuardian(config=cfg),
        "paper4": ExplainableTrustCalibrationEngine(config=cfg),
    }


@st.cache_data
def build_research_metrics() -> Dict[str, Dict[str, float]]:
    engines = get_backend_engines()

    paper1_case = {
        "severity_index": 0.68,
        "shock_index": 0.71,
        "gcs": 12.0,
        "lactate": 2.9,
        "mean_arterial_pressure": 72.0,
    }
    paper2_case = {
        "complexity": 0.61,
        "vitals_instability": 0.58,
        "comorbidity_load": 0.44,
    }
    paper3_case = {
        "severity_index": 0.63,
        "comorbidity_load": 0.47,
        "polypharmacy_index": 0.41,
        "renal_risk": 0.33,
    }
    paper4_case = {
        "explanation_coverage": 0.86,
        "auditability": 0.81,
        "hitl_presence": 0.89,
        "guideline_match": 0.87,
    }

    p1 = engines["paper1"].run_consistency_pipeline(paper1_case)
    p2 = engines["paper2"].run_htd_pipeline(paper2_case)
    p3 = engines["paper3"].verify_recommendation_path(paper3_case)
    p4 = engines["paper4"].run_trust_calibration(paper4_case)

    return {
        "paper1": {
            "innovation": float(p1["inter_agent_agreement_rate"]),
            "baseline": 74.2,
        },
        "paper2": {
            "innovation_time": float(p2["decision_time_seconds"]),
            "baseline_time": 21.6,
            "innovation_accuracy": float(p2["accuracy_rate_percent"]),
            "baseline_accuracy": 79.4,
        },
        "paper3": {
            "innovation": float(p3["unsafe_recommendation_rate_percent"]),
            "baseline": 16.1,
        },
        "paper4": {
            "innovation": float(p4["clinician_trust_score_percent"]),
            "baseline": 58.7,
        },
    }


def apply_style() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

            .stApp {
                background:
                    radial-gradient(circle at 10% 10%, #e1f6ff 0%, transparent 30%),
                    radial-gradient(circle at 90% 15%, #e8f1ff 0%, transparent 28%),
                    linear-gradient(180deg, #f9fbff 0%, #f2f7fd 55%, #edf3fa 100%);
                color: #0f2844;
                font-family: 'Manrope', sans-serif;
            }

            .block-container {
                padding-top: 1.0rem;
                padding-bottom: 2.0rem;
            }

            .hero {
                background: linear-gradient(130deg, #0f3f63 0%, #0f7b8f 55%, #1a6a98 100%);
                border: 1px solid rgba(255, 255, 255, 0.28);
                border-radius: 16px;
                color: #f7fbff;
                padding: 1rem 1.2rem;
                margin-bottom: 1rem;
                box-shadow: 0 16px 36px rgba(10, 40, 64, 0.17);
            }

            .hero-title {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.45rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }

            .hero-sub {
                font-size: 0.92rem;
                opacity: 0.95;
            }

            .pico-card {
                background: #ffffff;
                border: 1px solid #d9e5f2;
                border-radius: 12px;
                padding: 0.85rem;
                min-height: 126px;
                box-shadow: 0 8px 20px rgba(12, 42, 68, 0.06);
            }

            .pico-label {
                font-family: 'Space Grotesk', sans-serif;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 0.74rem;
                color: #0f7b8f;
                margin-bottom: 0.4rem;
            }

            .pico-value {
                color: #15314f;
                font-size: 0.9rem;
                line-height: 1.35;
            }

            .meta-row {
                border: 1px solid #d9e5f2;
                background: #ffffffd9;
                border-radius: 10px;
                padding: 0.75rem 0.9rem;
                margin-bottom: 0.7rem;
                color: #28435f;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Trauma Emergency Multi-Agent Research Dashboard</div>
            <div class="hero-sub">Dashboard + 4 paper views with production-style backend modules and simulation run controls</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pico(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="pico-card">
            <div class="pico-label">{label}</div>
            <div class="pico-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_simulation_button(paper_id: str, tab_name: str) -> None:
    key = f"run_{paper_id}"
    if st.button(f"Run {tab_name}", key=key, use_container_width=True):
        with st.spinner("Simulating backend execution... (2 second demo)"):
            time.sleep(2)
        st.session_state[f"{paper_id}_last"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"{tab_name} completed successfully.")

    last_key = f"{paper_id}_last"
    if last_key in st.session_state:
        st.info(f"Last simulated run: {st.session_state[last_key]}")


def render_dashboard(metrics: Dict[str, Dict[str, float]]) -> None:
    st.subheader("Dashboard")
    st.caption("Summary metrics for all 4 research papers")

    p1 = metrics["paper1"]
    p2 = metrics["paper2"]
    p3 = metrics["paper3"]
    p4 = metrics["paper4"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Paper 1: Inter-Agent Agreement", f"{p1['innovation']:.1f}%", f"+{(p1['innovation'] - p1['baseline']):.1f}%")
    with c2:
        st.metric("Paper 2: Decision Time", f"{p2['innovation_time']:.1f}s", f"-{(p2['baseline_time'] - p2['innovation_time']):.1f}s")
        st.metric("Paper 2: Accuracy", f"{p2['innovation_accuracy']:.1f}%", f"+{(p2['innovation_accuracy'] - p2['baseline_accuracy']):.1f}%")
    with c3:
        st.metric("Paper 3: Unsafe Rate", f"{p3['innovation']:.1f}%", f"-{(p3['baseline'] - p3['innovation']):.1f}%")
    with c4:
        st.metric("Paper 4: Clinician Trust", f"{p4['innovation']:.1f}%", f"+{(p4['innovation'] - p4['baseline']):.1f}%")

    bar_df = pd.DataFrame(
        {
            "Paper": ["Paper 1", "Paper 2", "Paper 3", "Paper 4"],
            "Innovation": [
                p1["innovation"],
                p2["innovation_accuracy"],
                100.0 - p3["innovation"],
                p4["innovation"],
            ],
            "Baseline": [
                p1["baseline"],
                p2["baseline_accuracy"],
                100.0 - p3["baseline"],
                p4["baseline"],
            ],
        }
    )

    st.bar_chart(bar_df.set_index("Paper"), height=320)

    trend_df = pd.DataFrame(
        [
            {"Step": 1, "Paper 1": p1["baseline"], "Paper 2": p2["baseline_accuracy"], "Paper 3": 100.0 - p3["baseline"], "Paper 4": p4["baseline"]},
            {"Step": 2, "Paper 1": (p1["baseline"] + p1["innovation"]) / 2.0, "Paper 2": (p2["baseline_accuracy"] + p2["innovation_accuracy"]) / 2.0, "Paper 3": 100.0 - ((p3["baseline"] + p3["innovation"]) / 2.0), "Paper 4": (p4["baseline"] + p4["innovation"]) / 2.0},
            {"Step": 3, "Paper 1": p1["innovation"], "Paper 2": p2["innovation_accuracy"], "Paper 3": 100.0 - p3["innovation"], "Paper 4": p4["innovation"]},
        ]
    )
    st.line_chart(trend_df, x="Step", y=["Paper 1", "Paper 2", "Paper 3", "Paper 4"], height=260)


def render_paper_tab(paper: PaperRecord, metrics: Dict[str, Dict[str, float]]) -> None:
    st.subheader(paper.tab_name)

    st.markdown(
        f"""
        <div class="meta-row">
            <strong>S.No:</strong> 1 | <strong>Reg No:</strong> 3192421216 | <strong>Student Name:</strong> Harsh Limkar
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="meta-row">
            <strong>Project Title:</strong> {paper.project_title}
        </div>
        """,
        unsafe_allow_html=True,
    )

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        render_pico("Problem", paper.problem)
    with p2:
        render_pico("Intervention", paper.intervention)
    with p3:
        render_pico("Comparison", paper.comparison)
    with p4:
        render_pico("Outcome", paper.outcome)

    left, right = st.columns([1, 1])
    with left:
        if paper.paper_id == "paper1":
            m = metrics["paper1"]
            st.metric("Inter-Agent Agreement Rate", f"{m['innovation']:.1f}%", f"+{(m['innovation'] - m['baseline']):.1f}%")
        elif paper.paper_id == "paper2":
            m = metrics["paper2"]
            st.metric("Decision Time", f"{m['innovation_time']:.1f}s", f"-{(m['baseline_time'] - m['innovation_time']):.1f}s")
            st.metric("Accuracy Rate", f"{m['innovation_accuracy']:.1f}%", f"+{(m['innovation_accuracy'] - m['baseline_accuracy']):.1f}%")
        elif paper.paper_id == "paper3":
            m = metrics["paper3"]
            st.metric("Unsafe Recommendation Rate", f"{m['innovation']:.1f}%", f"-{(m['baseline'] - m['innovation']):.1f}%")
        else:
            m = metrics["paper4"]
            st.metric("Clinician Trust Score", f"{m['innovation']:.1f}%", f"+{(m['innovation'] - m['baseline']):.1f}%")

    with right:
        run_simulation_button(paper.paper_id, paper.tab_name)


def main() -> None:
    st.set_page_config(page_title="Trauma Research Dashboard", page_icon="📊", layout="wide")
    apply_style()
    render_hero()

    metrics = build_research_metrics()

    dashboard_tab, rp1_tab, rp2_tab, rp3_tab, rp4_tab = st.tabs(
        ["Dashboard", "Research Paper 1", "Research Paper 2", "Research Paper 3", "Research Paper 4"]
    )

    with dashboard_tab:
        render_dashboard(metrics)
    with rp1_tab:
        render_paper_tab(PAPERS[0], metrics)
    with rp2_tab:
        render_paper_tab(PAPERS[1], metrics)
    with rp3_tab:
        render_paper_tab(PAPERS[2], metrics)
    with rp4_tab:
        render_paper_tab(PAPERS[3], metrics)


if __name__ == "__main__":
    main()
