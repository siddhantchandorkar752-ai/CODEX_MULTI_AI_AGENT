from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st


DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"


def get_secret_or_env(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    return str(value or os.getenv(name, default)).strip()


def api_base_url() -> str:
    configured = get_secret_or_env("OMEGA_API_BASE_URL", DEFAULT_API_BASE_URL)
    return configured.rstrip("/")


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


def render_connection_status() -> None:
    ok, result = api_get("/healthz")
    if ok:
        st.success(f"Backend connected: {api_base_url()}")
        return

    st.warning("Backend is not reachable from this Streamlit app.")
    with st.expander("Connection details", expanded=False):
        st.write(result)
        st.code(f"OMEGA_API_BASE_URL={api_base_url()}", language="text")
        st.caption(
            "For Streamlit Cloud, deploy the FastAPI backend separately and set "
            "OMEGA_API_BASE_URL in Streamlit secrets."
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
        else:
            st.error("Could not create a research run.")
            st.code(str(result), language="text")


def render_run_status() -> None:
    run_id = st.session_state.get("run_id")
    if not run_id:
        st.info("No run has been started in this Streamlit session.")
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

    with source_tab:
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
        st.markdown(
            """
            ### Report Draft

            The report stream will appear here after the Writer, Critic, and Verification
            agents are wired to the orchestration graph.
            """
        )

    with trace_tab:
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

    with st.sidebar:
        st.header("Runtime")
        st.text_input("API Base URL", value=api_base_url(), disabled=True)
        render_connection_status()
        st.divider()
        st.write("Set `OMEGA_API_BASE_URL` in Streamlit secrets for deployment.")

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
