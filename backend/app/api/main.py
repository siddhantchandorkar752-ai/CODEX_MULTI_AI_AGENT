from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, Field

from app.orchestration.state import RunState


app = FastAPI(title="Omega Research Grid API", version="0.1.0")


class CreateRunRequest(BaseModel):
    objective: str = Field(min_length=3)
    max_usd: float = Field(default=5.0, gt=0)
    max_wall_seconds: int = Field(default=900, gt=0)
    depth: str = "standard"


class CreateRunResponse(BaseModel):
    run_id: UUID
    state: RunState


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "omega-research-grid-api"}


@app.post("/v1/runs", response_model=CreateRunResponse)
async def create_run(request: CreateRunRequest) -> CreateRunResponse:
    # Persist run, enqueue orchestration start, and emit initial trace in production.
    return CreateRunResponse(run_id=uuid4(), state=RunState.PLANNING)


@app.get("/v1/runs/{run_id}")
async def get_run(run_id: UUID) -> dict[str, str]:
    return {"run_id": str(run_id), "state": RunState.PLANNING.value}


@app.post("/v1/runs/{run_id}/cancel")
async def cancel_run(run_id: UUID) -> dict[str, str]:
    return {"run_id": str(run_id), "status": "cancellation_requested"}


@app.websocket("/ws/runs/{run_id}")
async def run_stream(websocket: WebSocket, run_id: UUID) -> None:
    await websocket.accept()
    await websocket.send_json({"run_id": str(run_id), "event": "connected"})
    await websocket.close()
