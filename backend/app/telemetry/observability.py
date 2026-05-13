from __future__ import annotations

from contextlib import asynccontextmanager
from time import perf_counter
from typing import AsyncIterator

from app.schemas.messages import AgentName


@asynccontextmanager
async def agent_span(agent: AgentName, operation: str) -> AsyncIterator[dict[str, float | str]]:
    start = perf_counter()
    span: dict[str, float | str] = {"agent": agent.value, "operation": operation}
    try:
        yield span
        span["status"] = "ok"
    except Exception:
        span["status"] = "error"
        raise
    finally:
        span["latency_ms"] = (perf_counter() - start) * 1000
        # Replace with OpenTelemetry span attributes and Prometheus metrics.
