# Streamlit Frontend Deployment

The Streamlit app is a deployable frontend for Omega Research Grid. It lives at the repository root as `streamlit_app.py` because Streamlit Cloud expects a root entrypoint.

## Local Run

Run the FastAPI backend in one terminal:

```powershell
.\scripts\start_backend.ps1
```

Run Streamlit in another terminal:

```powershell
.\scripts\start_streamlit.ps1
```

Open:

```text
http://127.0.0.1:8501
```

## Streamlit Cloud Deployment

1. Push this repository to GitHub.
2. Create a new Streamlit Cloud app.
3. Select `streamlit_app.py` as the entrypoint.
4. Optional: add this secret after the FastAPI backend is deployed:

```toml
OMEGA_API_BASE_URL = "https://your-deployed-fastapi-backend.example.com"
```

5. Add provider API keys only when the backend or frontend code actually needs them.

The Streamlit frontend has demo mode enabled by default, so the public app can open and show the research operations console even when no backend or secrets are configured. Set this only if you want to force backend connectivity:

```toml
OMEGA_DEMO_MODE = "false"
```

## Important Backend Note

Streamlit Cloud runs the Streamlit process, not the FastAPI backend. For production, deploy the backend separately using one of:

- Render
- Railway
- Fly.io
- Azure App Service
- AWS ECS
- Kubernetes
- Docker on a VPS

Then point `OMEGA_API_BASE_URL` to that backend.

## Local Secrets

For local development, copy:

```text
.streamlit/secrets.example.toml
```

to:

```text
.streamlit/secrets.toml
```

Never commit `.streamlit/secrets.toml`.

Secrets are not required for the Streamlit UI to open. The app first checks environment variables. It only reads `st.secrets` when a local secrets file exists, which avoids Streamlit's "No secrets found" warning on clean machines.
