$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . ".\.venv\Scripts\Activate.ps1"
}

$env:OMEGA_API_BASE_URL = "http://127.0.0.1:8010"
streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501
