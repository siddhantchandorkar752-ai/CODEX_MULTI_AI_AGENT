# Testing and API Keys

## What Has Been Tested

Completed:

- Python syntax compilation for `backend` and `tests`.
- Static workspace structure check.

Not completed yet:

- `pytest` run, because `pytest` is not installed in the active Python environment.
- Frontend runtime verification, because `npm install` timed out and left partial install state, which was cleaned up.
- Live provider tests, because no API keys are configured.

## API Keys

Create a local `.env` from `.env.example` and fill only the providers you want to use.

Required for real AI runs:

- `OPENAI_API_KEY`

Optional by provider:

- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `TAVILY_API_KEY`
- `SERPAPI_API_KEY`
- `FIRECRAWL_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `LANGCHAIN_API_KEY`

Never commit `.env`.

Semantic Scholar note:

- `SEMANTIC_SCHOLAR_API_KEY` is optional for many Academic Graph endpoints.
- If you cannot get a key yet, leave it blank and use unauthenticated requests with stricter rate limiting.
- Some Semantic Scholar endpoints require authentication, so production deployments should still support the key when available.

## Backend Smoke Test

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:PYTHONPATH="backend"
pytest
uvicorn app.api.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Windows venv Fallback

If `python -m venv .venv` hangs while running `ensurepip`, or if you interrupt it with `Ctrl+C`, delete the partial environment and recreate it:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv --without-pip
.\.venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```

If `ensurepip` still hangs, use the system Python temporarily for the smoke test:

```powershell
$env:PYTHONPATH="backend"
python -m compileall -q backend tests
python -c "from app.orchestration.state import RunState, assert_transition; assert_transition(RunState.IDLE, RunState.PLANNING); print('smoke ok')"
```

Create a run:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/v1/runs `
  -ContentType "application/json" `
  -Body '{"objective":"Research the state of autonomous AI research agents","max_usd":1,"depth":"standard"}'
```

## Frontend Smoke Test

```powershell
cd frontend
npm install
npm run dev
```

Then open:

```text
http://127.0.0.1:3000
```

## Docker Smoke Test

```powershell
docker compose -f infra\docker-compose.yml up --build
```

Then open:

- API: `http://127.0.0.1:8000/docs`
- Frontend: `http://127.0.0.1:3000`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3001`
