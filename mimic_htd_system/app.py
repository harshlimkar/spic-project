"""Research dashboard frontend application for four trauma AI papers.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

import pandas as pd
import streamlit as st

# Backend connectors are intentionally referenced for architecture visibility.
# Frontend run buttons use UI-only simulation and do not invoke these classes.
from backend.paper1.role_based_consistency_engine import RoleBasedConsistencyEngine
from backend.paper2.htd_decision_latency_engine import HTDDecisionLatencyEngine
from backend.paper3.verification_safety_guardian import VerificationSafetyGuardian
from backend.paper4.explainable_trust_calibration_engine import ExplainableTrustCalibrationEngine


@dataclass(frozen=True)
class PaperConfig:
    paper_id: str
    tab_name: str
    project_title: str
    problem: str
    intervention: str
    comparison: str
    outcome: str
    primary_metric_label: str
    primary_metric_value: float
    baseline_value: float
    unit: str
    better_direction: str


PAPERS: List[PaperConfig] = [
    PaperConfig(
        paper_id="paper1",
        tab_name="Research Paper 1",
        project_title=(
            "Role-Based Multi-Agent AI Architecture for Trauma Emergency Decisions "
            "Compared to Traditional AI Systems with Improved Decision Consistency"
        ),
        problem="Decision Support Systems for Trauma emergency care",
        intervention="Role-Based Multi-Agent System (RB-MAS)",
        comparison="Monolithic AI architectures and rule-based trauma scoring systems",
        outcome="Inter-Agent Agreement Rate (%)",
        primary_metric_label="Inter-Agent Agreement Rate",
        primary_metric_value=92.4,
        baseline_value=73.6,
        unit="%",
        better_direction="higher",
    ),
    PaperConfig(
        paper_id="paper2",
        tab_name="Research Paper 2",
        project_title=(
            "Task-Based Multi-Agent Approach for Trauma Emergency Decision-Making "
            "Compared to Uncoordinated Workflows, Reducing Decision Time"
        ),
        problem="Poor coordination in trauma decision-making",
        intervention="Hierarchical Task Decomposition (HTD) with multi-agent planning",
        comparison="Sequential decision pipelines and uncoordinated AI/manual workflows",
        outcome="Average Decision Time (seconds) and Accuracy Rate (%)",
        primary_metric_label="Decision Accuracy Rate",
        primary_metric_value=95.1,
        baseline_value=79.2,
        unit="%",
        better_direction="higher",
    ),
    PaperConfig(
        paper_id="paper3",
        tab_name="Research Paper 3",
        project_title=(
            "Verification-Based Agentic AI System for Trauma Emergency Decisions Compared "
            "to Standard AI, Reducing Unsafe Recommendations"
        ),
        problem="Unsafe AI decisions in trauma care",
        intervention="Verification-Driven Agentic AI",
        comparison="Direct-prediction AI systems without validation layers",
        outcome="Unsafe Recommendation Rate (%)",
        primary_metric_label="Unsafe Recommendation Rate",
        primary_metric_value=2.7,
        baseline_value=16.4,
        unit="%",
        better_direction="lower",
    ),
    PaperConfig(
        paper_id="paper4",
        tab_name="Research Paper 4",
        project_title=(
            "Explainable Human-in-the-Loop Agentic AI System for Trauma Emergency "
            "Decisions Compared to Black-Box AI, Increasing Clinician Trust"
        ),
        problem="Lack of trust in trauma AI systems",
        intervention="Agent-Level Explainable AI (XAI) with Human-in-the-Loop (HITL) control",
        comparison="Black-box AI decision-support systems",
        outcome="Clinician Trust Score (%)",
        primary_metric_label="Clinician Trust Score",
        primary_metric_value=88.6,
        baseline_value=57.9,
        unit="%",
        better_direction="higher",
    ),
]


BACKEND_CONNECTORS: Dict[str, str] = {
    "paper1": RoleBasedConsistencyEngine.__name__,
    "paper2": HTDDecisionLatencyEngine.__name__,
    "paper3": VerificationSafetyGuardian.__name__,
    "paper4": ExplainableTrustCalibrationEngine.__name__,
}


def _delta_label(config: PaperConfig) -> str:
    delta = config.primary_metric_value - config.baseline_value
    if config.better_direction == "lower":
        delta = config.baseline_value - config.primary_metric_value
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}{config.unit} vs baseline"


def build_dashboard_frame() -> pd.DataFrame:
    records = []
    for item in PAPERS:
        records.append(
            {
                "Paper": item.tab_name,
                "Metric": item.primary_metric_label,
                "Current": item.primary_metric_value,
                "Baseline": item.baseline_value,
            }
        )
    return pd.DataFrame(records)


def apply_global_style() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

            :root {
                --bg-01: #f6f8fc;
                --bg-02: #ffffff;
                --ink-01: #10243f;
                --ink-02: #4f6279;
                --accent: #0f7b8f;
                --accent-soft: #dff4f7;
                --line: #dce4ef;
                --good: #2a9d4b;
                --warn: #d1495b;
            }

            .stApp {
                background:
                    radial-gradient(circle at 12% 18%, #dff4f7 0%, transparent 26%),
                    radial-gradient(circle at 92% 8%, #dce6ff 0%, transparent 24%),
                    linear-gradient(180deg, #f9fbff 0%, #f3f7fc 60%, #eef3f9 100%);
                color: var(--ink-01);
                font-family: 'Manrope', sans-serif;
            }

            .block-container {
                padding-top: 1.2rem;
                padding-bottom: 2.4rem;
            }

            .hero-wrap {
                background: linear-gradient(135deg, #083654 0%, #0f7b8f 45%, #1e6f9b 100%);
                color: #f7fbff;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 1rem 1.2rem;
                box-shadow: 0 14px 36px rgba(15, 45, 76, 0.18);
                margin-bottom: 1rem;
            }

            .hero-title {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.55rem;
                font-weight: 700;
                letter-spacing: -0.3px;
                margin-bottom: 0.2rem;
            }

            .hero-sub {
                font-size: 0.95rem;
                opacity: 0.95;
            }

            .pico-card {
                background: var(--bg-02);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.9rem;
                min-height: 124px;
                box-shadow: 0 8px 22px rgba(14, 43, 72, 0.06);
            }

            .pico-label {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 0.74rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: var(--accent);
                margin-bottom: 0.4rem;
            }

            .pico-value {
                color: var(--ink-01);
                line-height: 1.4;
                font-size: 0.9rem;
            }

            .meta-row {
                background: #ffffffd1;
                border: 1px solid var(--line);
                border-radius: 10px;
                padding: 0.8rem 0.9rem;
                margin: 0.8rem 0;
                color: var(--ink-02);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-title">Trauma Emergency Research Dashboard</div>
            <div class="hero-sub">Four-paper comparative view in PICO format with UI simulation controls</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    st.subheader("Dashboard")
    st.caption("Summary metrics for all four research papers")

    df = build_dashboard_frame()
    columns = st.columns(4)

    for col, item in zip(columns, PAPERS):
        with col:
            st.metric(
                label=item.primary_metric_label,
                value=f"{item.primary_metric_value:.1f}{item.unit}",
                delta=_delta_label(item),
            )

    bar_data = df[["Paper", "Current"]].set_index("Paper")
    st.bar_chart(bar_data, height=320)

    trend_rows = []
    for item in PAPERS:
        for run_step in range(1, 6):
            if item.better_direction == "lower":
                value = max(item.primary_metric_value, item.baseline_value - (run_step * 2.8))
            else:
                value = min(item.primary_metric_value, item.baseline_value + (run_step * 5.9))
            trend_rows.append({"Paper": item.tab_name, "Step": run_step, "Value": round(value, 2)})

    trend_df = pd.DataFrame(trend_rows)
    st.line_chart(trend_df, x="Step", y="Value", color="Paper", height=280)


def render_pico_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="pico-card">
            <div class="pico-label">{label}</div>
            <div class="pico-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def simulate_frontend_run(paper: PaperConfig) -> None:
    run_key = f"{paper.paper_id}_last_run"
    if st.button(f"Run {paper.tab_name}", key=f"run_{paper.paper_id}", use_container_width=True):
        with st.spinner("Simulating backend execution... (2 second demo window)"):
            time.sleep(2)
        st.session_state[run_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"{paper.tab_name} completed successfully.")

    if run_key in st.session_state:
        st.info(f"Last simulated run: {st.session_state[run_key]}")


def render_paper_page(paper: PaperConfig) -> None:
    st.subheader(paper.tab_name)

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
        render_pico_card("Problem", paper.problem)
    with p2:
        render_pico_card("Intervention", paper.intervention)
    with p3:
        render_pico_card("Comparison", paper.comparison)
    with p4:
        render_pico_card("Outcome", paper.outcome)

    metric_col, run_col = st.columns([1, 1])
    with metric_col:
        st.metric(
            label=paper.primary_metric_label,
            value=f"{paper.primary_metric_value:.1f}{paper.unit}",
            delta=_delta_label(paper),
        )

        if paper.paper_id == "paper2":
            st.metric("Decision Time", "6.2s", "-14.6s vs baseline")

    with run_col:
        simulate_frontend_run(paper)

    with st.expander("Backend module mapping", expanded=False):
        st.write(f"Connected backend component: {BACKEND_CONNECTORS[paper.paper_id]}")
        st.caption("This UI intentionally runs simulation-only behavior from the frontend layer.")


def main() -> None:
    st.set_page_config(
        page_title="Trauma Research Dashboard",
        page_icon="📊",
        layout="wide",
    )
    apply_global_style()
    render_header()

    dashboard_tab, paper1_tab, paper2_tab, paper3_tab, paper4_tab = st.tabs(
        ["Dashboard", "Research Paper 1", "Research Paper 2", "Research Paper 3", "Research Paper 4"]
    )

    with dashboard_tab:
        render_dashboard()
    with paper1_tab:
        render_paper_page(PAPERS[0])
    with paper2_tab:
        render_paper_page(PAPERS[1])
    with paper3_tab:
        render_paper_page(PAPERS[2])
    with paper4_tab:
        render_paper_page(PAPERS[3])


if __name__ == "__main__":
    main()
