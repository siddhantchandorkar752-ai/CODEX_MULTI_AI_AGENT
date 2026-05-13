from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import requests
import streamlit as st


DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
DEMO_RUN_PREFIX = "demo-"


def get_secret_or_env(name: str, default: str = "") -> str:
    env_value = os.getenv(name)
    if env_value:
        return env_value.strip()

    local_secret_paths = [
        Path.cwd() / ".streamlit" / "secrets.toml",
        Path.home() / ".streamlit" / "secrets.toml",
    ]
    if any(path.exists() for path in local_secret_paths):
        try:
            secret_value = st.secrets.get(name)
        except Exception:
            secret_value = None
        if secret_value:
            return str(secret_value).strip()

    return default.strip()


def api_base_url() -> str:
    configured = get_secret_or_env("OMEGA_API_BASE_URL", DEFAULT_API_BASE_URL)
    return configured.rstrip("/")


def demo_mode_enabled() -> bool:
    configured = get_secret_or_env("OMEGA_DEMO_MODE", "true").lower()
    return configured not in {"0", "false", "no", "off"}


def api_get(path: str, timeout: float = 4.0) -> tuple[bool, dict[str, Any] | str]:
    try:
        response = requests.get(f"{api_base_url()}{path}", timeout=timeout)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as exc:
        return False, str(exc)


def api_post(path: str, payload: dict[str, Any], timeout: float = 15.0) -> tuple[bool, dict[str, Any] | str]:
    try:
        response = requests.post(f"{api_base_url()}{path}", json=payload, timeout=timeout)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as exc:
        return False, str(exc)


def generate_demo_report(objective: str) -> str:
    normalized = objective.lower().strip()
    if "capital" in normalized and "france" in normalized:
        return """
### Executive Summary

Paris is the capital of France.

### Methodology

This is a stable factual question. The demo answers directly instead of pretending to perform a full research workflow.

### Answer

Paris.

### Confidence

**High.** This is stable general knowledge and does not require live web retrieval.
"""

    if all(term in normalized for term in ["langgraph", "crewai", "autogen"]) or "semantic kernel" in normalized:
        return """
### Executive Summary

For a production-grade multi-agent research assistant, **LangGraph is the strongest default architecture**. It gives explicit state graphs, checkpointing, deterministic routing, resumable execution, and clearer operational control than role-chat frameworks. CrewAI is useful for fast role-based prototypes, AutoGen is strong for conversational multi-agent experiments, and Semantic Kernel is attractive for enterprise plugin ecosystems, especially in Microsoft/.NET-heavy environments. For this project, LangGraph plus LCEL inside nodes is the best fit.

### Comparison

| Framework | Best Use | Strengths | Weaknesses |
|---|---|---|---|
| LangGraph | Production agent orchestration | Explicit state machines, checkpoints, graph routing, retries, human interrupts | Requires careful schema and state design |
| CrewAI | Fast agent-role prototypes | Simple mental model, quick setup, readable role/task abstractions | Less deterministic, weaker for replay and strict governance |
| AutoGen | Multi-agent conversation research | Flexible agent-to-agent dialogue, good experimentation surface | Harder to bound, test, audit, and cost-control in production |
| Semantic Kernel | Enterprise app/plugin integration | Strong plugin orientation, good fit for Microsoft ecosystems | Less native for LangChain/LangGraph retrieval workflows |

### Recommendation

Use **LangGraph as the orchestration layer**, **LCEL for internal chains**, and a custom governance kernel around budgets, permissions, retries, and evaluation gates.

The production shape should be:

1. Planner node creates an execution DAG.
2. Search and Reader nodes run concurrently with bounded retries.
3. Memory node assembles verified context.
4. Writer node drafts a cited report.
5. Critic and Verification nodes run quality gates.
6. Finalizer emits report, traces, citations, costs, and confidence scores.

### Tradeoffs

LangGraph costs more design effort upfront because state schemas, transitions, and checkpoint behavior must be explicit. That is a good trade for enterprise systems: debugging, replay, cancellation, audit, and observability become possible. CrewAI and AutoGen can feel more natural early, but they tend to become difficult to govern when the system needs strict cost limits, deterministic transitions, and failure recovery.

### Scalability Implications

LangGraph maps cleanly onto distributed workers because each node has typed inputs and outputs. Search, reading, extraction, and verification can scale horizontally behind queues. The bottlenecks shift from orchestration logic to provider rate limits, vector database latency, PDF extraction throughput, and model-token cost.

### Production Risks

The main risks are graph deadlocks, stale checkpoints, runaway retries, inconsistent model outputs, source poisoning, and excessive token spend. These should be handled with state transition validation, idempotency keys, circuit breakers, source sanitization, cost accounting, and evaluation thresholds.

### Final Decision

Choose **LangGraph + LCEL + custom governance**. It is the best balance of determinism, observability, extensibility, and production control for a multi-agent research operating system.

### Confidence

**High for architectural direction.** This demo response is based on framework design characteristics, not live benchmark execution.
"""

    if "multi-agent" in normalized or "autonomous" in normalized or "agentic" in normalized:
        return """
### Executive Summary

Autonomous multi-agent AI systems are moving from simple role-based chat loops toward governed execution graphs. The strongest architectures combine deterministic orchestration, tool isolation, retrieval pipelines, shared memory, citation verification, telemetry, and evaluation gates. The frontier pattern is not one big chatbot; it is a supervised network of specialized workers operating under a policy kernel.

### Major Architectures

1. **Graph-based orchestration:** Explicit DAGs or finite-state machines coordinate planning, retrieval, writing, critique, and verification.
2. **Role-based collaboration:** Agents are assigned roles such as Planner, Searcher, Reader, Writer, and Critic.
3. **Tool-using research loops:** Agents call search, browsers, databases, code execution, and document parsers.
4. **Memory-augmented systems:** Short-term working memory and long-term vector memory help preserve context across runs.
5. **Evaluator-supervised systems:** Critic and verification agents score factuality, citation quality, reasoning, and confidence.

### Enterprise Use Cases

- Competitive intelligence and market research.
- Scientific and technical literature review.
- Legal and regulatory monitoring.
- Due diligence and investment research.
- Internal knowledge synthesis across documents, tickets, and wikis.
- Automated report generation with citation trails.

### Key Risks

- Hallucinated claims and fake citations.
- Prompt injection from webpages and PDFs.
- Runaway model/tool costs.
- Poor observability during multi-step failures.
- Cross-tenant memory leakage.
- Over-trusting low-quality retrieved sources.

### Production Requirements

A serious system needs deterministic orchestration, typed messages, budget enforcement, source sanitization, retrieval evaluation, trace logging, confidence scoring, dead-letter queues, circuit breakers, and human escalation paths.

### Outlook

The near-term winners will be systems that combine autonomy with governance. Fully unbounded agents are risky; supervised, observable, stateful agent networks are deployable.

### Confidence

**Medium-high.** This is a demo synthesis based on the architecture scaffold, not live web retrieval.
"""

    return """
### Executive Summary

The public demo has accepted the research objective and generated a structured preview. A deployed backend is required for live internet search, retrieval, citation verification, and model-powered synthesis.

### Preview Workflow

1. Planner creates a bounded research task.
2. Search and Reader stages would collect evidence.
3. Memory would assemble verified context.
4. Writer would draft the report.
5. Critic and Verification would check factuality and citations.

### Current Limitation

This Streamlit deployment is running without a public FastAPI backend, so it cannot perform live retrieval or real model calls yet.

### Next Step

Deploy the FastAPI backend and set `OMEGA_API_BASE_URL` in Streamlit Cloud secrets or environment variables.

### Confidence

**Preview only.** No live internet retrieval is performed in public demo mode.
"""


def generate_demo_sources(objective: str) -> list[dict[str, Any]]:
    normalized = objective.lower()
    if "capital" in normalized and "france" in normalized:
        return [
            {
                "source": "Built-in demo knowledge",
                "trust": 0.95,
                "status": "verified",
                "note": "Paris is the capital of France.",
            }
        ]
    if all(term in normalized for term in ["langgraph", "crewai", "autogen"]) or "semantic kernel" in normalized:
        return [
            {
                "source": "Architecture knowledge base",
                "trust": 0.82,
                "status": "demo synthesis",
                "note": "Compares framework design characteristics.",
            },
            {
                "source": "Omega blueprint",
                "trust": 0.86,
                "status": "local artifact",
                "note": "Recommends LangGraph + LCEL + governance kernel.",
            },
        ]
    if "multi-agent" in normalized or "autonomous" in normalized or "agentic" in normalized:
        return [
            {
                "source": "Omega architecture blueprint",
                "trust": 0.84,
                "status": "local artifact",
                "note": "Summarizes agentic system design patterns.",
            },
            {
                "source": "Demo synthesis engine",
                "trust": 0.70,
                "status": "demo synthesis",
                "note": "No live web retrieval in public demo mode.",
            },
        ]
    return [
        {
            "source": "Demo planner",
            "trust": 0.75,
            "status": "simulated",
            "note": "Objective decomposed for preview.",
        },
        {
            "source": "Live retrieval backend",
            "trust": 0.0,
            "status": "not connected",
            "note": "Set OMEGA_API_BASE_URL to enable real evidence retrieval.",
        },
    ]


def generate_demo_trace() -> list[dict[str, str]]:
    return [
        {"agent": "planner", "state": "completed", "event": "Objective accepted"},
        {"agent": "search", "state": "demo", "event": "Live search skipped in public demo mode"},
        {"agent": "reader", "state": "demo", "event": "Extraction skipped until backend is connected"},
        {"agent": "writer", "state": "completed", "event": "Readable demo report generated"},
        {"agent": "verification", "state": "demo", "event": "Marked as demo-scoped output"},
    ]


def create_demo_run(payload: dict[str, Any]) -> dict[str, Any]:
    run_id = f"{DEMO_RUN_PREFIX}{uuid4()}"
    st.session_state["demo_runs"][run_id] = {
        "run_id": run_id,
        "state": "FINALIZING",
        "objective": payload["objective"],
        "depth": payload["depth"],
        "max_usd": payload["max_usd"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "demo",
        "report": generate_demo_report(payload["objective"]),
        "sources": generate_demo_sources(payload["objective"]),
        "trace": generate_demo_trace(),
    }
    return st.session_state["demo_runs"][run_id]


def get_demo_run(run_id: str) -> dict[str, Any] | None:
    return st.session_state.get("demo_runs", {}).get(run_id)


def render_connection_status() -> None:
    ok, result = api_get("/healthz")
    if ok:
        st.session_state["backend_connected"] = True
        st.success(f"Backend connected: {api_base_url()}")
        return

    st.session_state["backend_connected"] = False
    if demo_mode_enabled():
        st.info("Demo mode active. The app can run without backend secrets or a deployed API.")
    else:
        st.warning("Backend is not reachable from this Streamlit app.")

    with st.expander("Connection details", expanded=False):
        st.write(result)
        st.code(f"OMEGA_API_BASE_URL={api_base_url()}", language="text")
        st.caption(
            "For production, deploy the FastAPI backend separately and set "
            "OMEGA_API_BASE_URL as an environment variable or Streamlit Cloud secret."
        )


def render_operator_summary() -> None:
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Run State", st.session_state.get("run_state", "IDLE"))
    col_b.metric("Agents", "8")
    col_c.metric("Budget", f"${st.session_state.get('max_usd', 5.0):.2f}")
    col_d.metric("Confidence Gate", "0.88")


def render_execution_graph() -> None:
    st.graphviz_chart(
        """
        digraph {
          rankdir=LR;
          node [shape=box, style="rounded,filled", fillcolor="#111827", fontcolor="#F9FAFB", color="#374151"];
          Planner -> Search -> Reader -> Memory -> Writer -> Critic -> Verification -> Finalizer;
          Critic -> Writer [label="revise", color="#10B981", fontcolor="#10B981"];
        }
        """
    )


def render_run_launcher() -> None:
    st.subheader("Research Run")

    objective = st.text_area(
        "Objective",
        value=st.session_state.get(
            "objective",
            "Research the current state of autonomous multi-agent research systems.",
        ),
        height=120,
    )

    col_a, col_b, col_c = st.columns([1, 1, 1])
    max_usd = col_a.number_input("Max USD", min_value=0.10, max_value=100.0, value=5.0, step=0.50)
    max_wall_seconds = col_b.number_input("Max seconds", min_value=60, max_value=7200, value=900, step=60)
    depth = col_c.selectbox("Depth", ["standard", "deep", "exhaustive"], index=0)

    st.session_state["max_usd"] = max_usd
    st.session_state["objective"] = objective

    if st.button("Start Research Run", type="primary", use_container_width=True):
        payload = {
            "objective": objective,
            "max_usd": max_usd,
            "max_wall_seconds": max_wall_seconds,
            "depth": depth,
        }
        ok, result = api_post("/v1/runs", payload)
        if ok and isinstance(result, dict):
            st.session_state["run_id"] = result.get("run_id")
            st.session_state["run_state"] = result.get("state", "PLANNING")
            st.success("Research run created.")
        elif demo_mode_enabled():
            demo_run = create_demo_run(payload)
            st.session_state["run_id"] = demo_run["run_id"]
            st.session_state["run_state"] = demo_run["state"]
            st.success("Demo research run created.")
        else:
            st.error("Could not create a research run.")
            st.code(str(result), language="text")


def render_run_status() -> None:
    run_id = st.session_state.get("run_id")
    if not run_id:
        st.info("No run has been started in this Streamlit session.")
        return

    if str(run_id).startswith(DEMO_RUN_PREFIX):
        demo_run = get_demo_run(str(run_id))
        if demo_run:
            st.success("Demo run completed.")
            col_a, col_b = st.columns(2)
            col_a.metric("Run ID", str(demo_run["run_id"])[:18] + "...")
            col_b.metric("State", demo_run["state"])
            st.caption(f"Objective: {demo_run['objective']}")
            return

    ok, result = api_get(f"/v1/runs/{run_id}")
    if ok and isinstance(result, dict):
        st.session_state["run_state"] = result.get("state", st.session_state.get("run_state", "UNKNOWN"))
        st.json(result)
    else:
        st.error("Could not fetch run status.")
        st.code(str(result), language="text")


def render_source_and_report_shell() -> None:
    source_tab, report_tab, trace_tab = st.tabs(["Sources", "Report", "Trace"])
    run_id = st.session_state.get("run_id")
    demo_run = get_demo_run(str(run_id)) if run_id and str(run_id).startswith(DEMO_RUN_PREFIX) else None

    with source_tab:
        if demo_run:
            st.dataframe(demo_run["sources"], use_container_width=True, hide_index=True)
        else:
            st.dataframe(
                [
                    {"source": "Search provider output", "trust": 0.0, "status": "pending"},
                    {"source": "Reader extracted claims", "trust": 0.0, "status": "pending"},
                    {"source": "Verification results", "trust": 0.0, "status": "pending"},
                ],
                use_container_width=True,
                hide_index=True,
            )

    with report_tab:
        if demo_run:
            st.markdown(demo_run["report"])
        else:
            st.markdown(
                """
                ### Report Draft

                Start a research run to generate a report preview.
                """
            )

    with trace_tab:
        if demo_run:
            st.dataframe(demo_run["trace"], use_container_width=True, hide_index=True)
        else:
            st.code(
                "Trace events will stream here after WebSocket support is connected to Streamlit.",
                language="text",
            )


def main() -> None:
    st.set_page_config(
        page_title="Omega Research Grid",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Omega Research Grid")
    st.caption("Autonomous multi-agent research operations console")
    st.session_state.setdefault("demo_runs", {})

    with st.sidebar:
        st.header("Runtime")
        st.text_input("API Base URL", value=api_base_url(), disabled=True)
        render_connection_status()
        st.divider()
        st.write("Public demo mode works without secrets. Set `OMEGA_API_BASE_URL` when a backend is deployed.")

    render_operator_summary()

    left, right = st.columns([0.95, 1.05], gap="large")
    with left:
        render_run_launcher()
        st.divider()
        render_run_status()

    with right:
        st.subheader("Execution Graph")
        render_execution_graph()

    st.divider()
    render_source_and_report_shell()


if __name__ == "__main__":
    main()
